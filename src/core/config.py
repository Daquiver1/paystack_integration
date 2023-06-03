"""Setting up configs."""

# Third party imports
import logging

from starlette.config import Config

config = Config(".env")


log = logging.getLogger(__name__)


PROJECT_NAME = "paystack-demo"
VERSION = "1.0"
API_PREFIX = "/api"

PAYSTACK_PUBLIC_KEY_DEV = config("PAYSTACK_PUBLIC_KEY_DEV")
PAYSTACK_SECRET_KEY_DEV = config("PAYSTACK_SECRET_KEY_DEV")
PAYSTACK_PUBLIC_KEY_PROD = config("PAYSTACK_PUBLIC_KEY_PROD")
PAYSTACK_SECRET_KEY_PROD = config("PAYSTACK_SECRET_KEY_PROD")