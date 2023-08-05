"""mse_lib_sgx.cli module."""

import argparse
import asyncio
from datetime import datetime, timedelta
from enum import Enum
import importlib
import os
import logging
import sys
from pathlib import Path
from typing import Type, Union

from cryptography import x509
from cryptography.x509.oid import NameOID
from hypercorn.asyncio import serve
from hypercorn.config import Config

from mse_lib_sgx import globs
from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate
from mse_lib_sgx.http_server import serve as serve_sgx_secrets
from mse_lib_sgx.import_hook import import_set_key


def parse_args() -> argparse.Namespace:
    """Argument parser."""
    parser = argparse.ArgumentParser(description="Start a MSE Enclave server.")
    parser.add_argument(
        "application",
        type=str,
        help="Application to dispatch to as path.to.module:instance.path")

    parser.add_argument("--host",
                        required=True,
                        type=str,
                        help="Hostname of the server")
    parser.add_argument("--port",
                        required=True,
                        type=int,
                        help="Port of the server")
    parser.add_argument(
        "--app-dir",
        required=True,
        type=Path,
        help="Path the microservice application. Read only directory")
    parser.add_argument(
        "--data-dir",
        required=True,
        type=Path,
        help="Path with data encrypted for a specific MRENCLAVE. "
        "Read/write directory")
    parser.add_argument("--debug",
                        action="store_true",
                        help="Debug mode without SGX")
    parser.add_argument("--encrypted-code",
                        action="store_true",
                        default=False,
                        help="Whether the application is encrypted")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--self-signed",
                       type=int,
                       metavar="EXPIRATION_DATE",
                       help="Generate a self-signed certificate for the app. "
                       "Specify the expiration date of the certificate "
                       "as a timestamp since Epoch.")

    group.add_argument("--no-ssl",
                       action="store_true",
                       help="Don't use HTTPS connection")

    group.add_argument(
        "--certificate",
        type=Path,
        metavar="CERTIFICATE_PATH",
        help="Use the given certificate for the SSL connection. "
        "the private key will be sent using the configuration server")

    return parser.parse_args()


class AppConnection(Enum):
    """Define the possible values to deal with the app connection."""

    ENCLAVE_CERTIFICATE = 1
    OWNER_CERTFICIATE = 2
    NO_SSL = 3


def run() -> None:
    """Entrypoint of the CLI.

    The program creates a self signed certificate.

    Then starts a configuration server using HTTPS and this previous cert
    in order to allow the user to send some secrets params.

    Once all the secrets has been sent, three options:
    - (--self-signed) If the app owner relies on the enclave certificate,
      then start the app server using this same certificate
    - (--certificate) Start the app server using the certificate
      provided by the app owner. In that case, the certificate
      is already present in the workspace of the program
      but the private key is sent by the app owner
      when the configuration server is up.
    - (--no-ssl) If the app owner and the users trust the operator (cosmian)
      then don't use https connection.
    """
    args: argparse.Namespace = parse_args()
    os.makedirs(args.data_dir, exist_ok=True)

    FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    ssl_private_key_path = None
    expiration_date = datetime.now() + timedelta(hours=10)
    if args.no_ssl:
        # The conf server use the self signed cert
        # No ssl for the app server
        app_connection = AppConnection.NO_SSL
    elif args.certificate:
        # The conf server use the self signed cert
        # The app server use the app owner cert
        app_connection = AppConnection.OWNER_CERTFICIATE
        ssl_private_key_path = args.data_dir / "key.app.pem"
    else:
        # The conf server and the app server will use the same self signed cert
        app_connection = AppConnection.ENCLAVE_CERTIFICATE
        expiration_date = datetime.utcfromtimestamp(args.self_signed)

    logging.info("Generating the self signed certificate...")

    subject: x509.Name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Ile-de-France"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Paris"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Cosmian Tech"),
        x509.NameAttribute(NameOID.COMMON_NAME, "cosmian.com"),
    ])

    cert_class: Union[Type[SGXCertificate], Type[
        SelfSignedCertificate]] = SGXCertificate if not args.debug \
        else SelfSignedCertificate
    cert: Union[SGXCertificate, SelfSignedCertificate] = cert_class(
        dns_name=args.host,
        subject=subject,
        root_path=Path(args.data_dir),
        expiration_date=expiration_date)

    if args.encrypted_code or app_connection == AppConnection.OWNER_CERTFICIATE:
        logging.info("Starting the configuration server...")

        # The app owner could send (both or a single):
        # - the key to decrypt the code if it's encrypted
        # - the SSL private key if it doesn't want to use our self-signed cert
        serve_sgx_secrets(
            hostname="0.0.0.0",
            port=args.port,
            certificate=cert,
            need_code_sealed_key=args.encrypted_code,
            need_ssl_private_key=(
                app_connection == AppConnection.OWNER_CERTFICIATE))

        if args.encrypted_code and globs.CODE_SEALED_KEY:
            import_set_key(globs.CODE_SEALED_KEY)

        if app_connection == AppConnection.OWNER_CERTFICIATE \
            and globs.SSL_PRIVATE_KEY \
                and ssl_private_key_path is not None:
            ssl_private_key_path.write_text(globs.SSL_PRIVATE_KEY)

    config_map = {
        "bind": f"0.0.0.0:{args.port}",
        "alpn_protocols": ["h2"],
        "workers": 1,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvloop",
        "wsgi_max_body_size": 2 * 1024 * 1024 * 1024  # 2 GB
    }

    if app_connection == AppConnection.OWNER_CERTFICIATE:
        config_map["certfile"] = args.certificate
        config_map["keyfile"] = ssl_private_key_path
    elif app_connection == AppConnection.ENCLAVE_CERTIFICATE:
        config_map["certfile"] = cert.cert_path
        config_map["keyfile"] = cert.key_path

    config = Config.from_mapping(config_map)

    logging.info("Loading the application (encrypted=%s)...",
                 "Yes" if args.encrypted_code else "No")
    sys.path.append(f"{args.app_dir.resolve()}")
    module, app = args.application.split(":")
    app = getattr(importlib.import_module(module), app)

    logging.info("Starting the application (mode=%s)...", app_connection.name)
    asyncio.run(serve(app, config))
