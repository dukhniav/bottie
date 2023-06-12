import logging
import threading
import time

from bottie import __version__

logger = logging.getLogger(__name__)


class Worker:
    def __init__(self) -> None:
        logger.info(f"Initializing worker (ver={__version__})")
        self._stop_event = threading.Event()
        self._worker_thread = None  # Initialize the worker thread variable

    def start(self) -> bool:
        logger.info("Starting worker...")
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._worker_loop)
        self._worker_thread.start()
        status = True
        return status

    def stop(self):
        logger.info("Stopping worker...")
        if self._worker_thread:
            self._worker_thread.join()  # Wait for the worker thread to finish

    # def stop(self) -> bool:
    #     logger.info("Stopping worker...")
    #     self._stop_event.set()
    #     self._worker_thread.join()  # Wait for the worker thread to finish
    #     self._worker_thread = None  # Reset the worker thread variable
    #     status = True
    #     return status

    def _worker_loop(self):

        while not self._stop_event.is_set():
            # Perform worker tasks
            time.sleep(1)  # Example: Simulate some work
        logger.info("Worker stopped.")
