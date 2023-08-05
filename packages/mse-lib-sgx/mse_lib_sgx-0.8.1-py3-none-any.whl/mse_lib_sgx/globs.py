"""mse_lib_sgx.global module."""

import threading
from typing import Optional

CODE_SEALED_KEY: Optional[bytes] = None
NEED_CODE_SEALED_KEY: bool = False

EXIT_EVENT: threading.Event = threading.Event()

SSL_PRIVATE_KEY: Optional[str] = None
NEED_SSL_PRIVATE_KEY: bool = False
