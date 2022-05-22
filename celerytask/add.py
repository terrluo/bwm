from celery.utils.log import get_task_logger

from bwm import celery

logger = get_task_logger(__name__)


@celery.task()
def add_together(a, b):
    logger.info("运行 add_together ...")
    return a + b
