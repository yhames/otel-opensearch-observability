import logging

import uvicorn

from app import create_app
from app.config import get_settings

settings = get_settings()
app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)


def run():
    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    run()
