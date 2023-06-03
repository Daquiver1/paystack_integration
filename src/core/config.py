"""Setting up configs."""

# Third party imports
import logging

from starlette.config import Config

config = Config(".env")


log = logging.getLogger(__name__)


PROJECT_NAME = "paystack-demo"
VERSION = "1.0"
API_PREFIX = "/api"

ENV = config("ENV")
BASE_URL = config("BASE_URL")

if ENV == "PROD":
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_PUBLIC_KEY_PROD")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY_PROD")
else:
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_PUBLIC_KEY_DEV")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY_DEV")
