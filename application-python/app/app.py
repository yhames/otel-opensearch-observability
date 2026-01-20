from fastapi import FastAPI

from app.config import setup_otel
from app.router import log_router


def create_app():
    app = FastAPI()

    # Setup OpenTelemetry
    setup_otel(app)

    # Include routers
    app.include_router(log_router)

    return app
