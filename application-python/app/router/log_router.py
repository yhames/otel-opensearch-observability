import logging
from fastapi import APIRouter, Depends

from app.service import ILogService, get_log_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/logs")


@router.get("/test")
def get_log_test(
        service: ILogService = Depends(get_log_service),
):
    logger.info("GET /logs/test called")
    service.log_test_service("This is a test log message from LogService.")
    return {"message": "Log test completed."}
