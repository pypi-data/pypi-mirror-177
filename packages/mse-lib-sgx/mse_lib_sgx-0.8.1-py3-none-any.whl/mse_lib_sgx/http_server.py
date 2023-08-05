"""mse_lib_sgx.http_server module."""

import json
import logging
import ssl
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Union

import nacl

from mse_lib_sgx import globs
from mse_lib_sgx.certificate import SelfSignedCertificate, SGXCertificate


class SGXHTTPRequestHandler(BaseHTTPRequestHandler):
    """SGX HTTP server to complete application config with secrets params."""

    def do_GET(self) -> None:
        """GET /."""
        msg: bytes = b"Waiting for sealed symmetric key and/or ssl private key..."
        self.send_response(200)
        self.send_header("Content-Length", str(len(msg)))
        # We send an extra header to easily know when the configuration server is up
        self.send_header("Mse-Status", "Waiting")
        self.end_headers()
        self.wfile.write(msg)

    def do_POST(self) -> None:
        """POST /."""
        logging.info("Processing POST query...")
        content_length: int = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        # body is a json with one or two of these fields:
        # - ssl_private_key
        # - code_sealed_key
        try:
            data = json.loads(body.decode('utf8'))

            if globs.NEED_SSL_PRIVATE_KEY:
                globs.SSL_PRIVATE_KEY = data["ssl_private_key"]

            if globs.NEED_CODE_SEALED_KEY:
                globs.CODE_SEALED_KEY = bytes.fromhex(data["code_sealed_key"])
                if len(globs.CODE_SEALED_KEY) != 32:
                    raise nacl.exceptions.CryptoError

        except (KeyError, ValueError, json.JSONDecodeError,
                nacl.exceptions.CryptoError, nacl.exceptions.TypeError) as exc:
            logging.error(exc)
            self.send_response_only(401)
            self.end_headers()
            return

        self.send_response_only(200)
        self.end_headers()
        globs.EXIT_EVENT.set()


def serve(hostname: str, port: int, certificate: Union[SGXCertificate,
                                                       SelfSignedCertificate],
          need_code_sealed_key: bool, need_ssl_private_key: bool):
    """Serve simple SGX HTTP server."""
    globs.NEED_CODE_SEALED_KEY = need_code_sealed_key
    globs.NEED_SSL_PRIVATE_KEY = need_ssl_private_key

    httpd = HTTPServer((hostname, port), SGXHTTPRequestHandler)

    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(
        certfile=str(certificate.cert_path.resolve()),
        keyfile=str(certificate.key_path.resolve()),
    )

    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    threading.Thread(target=kill_event, args=(httpd,)).start()
    httpd.serve_forever()


def kill_event(httpd: HTTPServer):
    """Kill HTTP server in a thread if `EXIT_EVENT` is set."""
    while True:
        if globs.EXIT_EVENT.is_set():
            logging.info("Stopping the configuration server...")
            httpd.shutdown()
            return

        time.sleep(1)
