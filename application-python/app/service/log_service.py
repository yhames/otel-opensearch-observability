from abc import ABC

import logging

logger = logging.getLogger(__name__)


class ILogService(ABC):
    def log_test_service(self, message: str) -> None:
        pass


class LogService(ILogService):
    def log_test_service(self, message: str) -> None:
        logger.info(f"LogService: {message}")


def get_log_service() -> ILogService:
    return LogService()
