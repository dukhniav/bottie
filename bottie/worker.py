import logging

from bottie import __version__

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self) -> None:
        logger.info(f"Initializing worker (ver={__version__})")

    def start(self) -> bool:
        logger.info("Starting worker...")
        status = True

        return status

    def stop(self) -> bool:
        logger.info("Stopping worker...")
        status = True

        return status
