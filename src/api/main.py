"""Server Setup."""

# Third party imports
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.routes.paystack import router as accept_payments_router
from src.core import config


def get_application() -> FastAPI:
    """Server configs."""
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", name="index")
    async def index() -> str:
        return "Application startup complete."

    app.include_router(accept_payments_router, prefix="/api")

    return app


app = get_application()
