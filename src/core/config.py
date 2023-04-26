"""Setting up configs."""

# Third party imports
import logging

from starlette.config import Config

config = Config(".env")


log = logging.getLogger(__name__)


PROJECT_NAME = "paystack-demo"
VERSION = "1.0"
API_PREFIX = "/api"

PAYSTACK_PUBLIC_KEY = config("PAYSTACK_PUBLIC_KEY")
PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY")
