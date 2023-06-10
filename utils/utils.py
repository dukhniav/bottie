import sched
import time
import threading
from logging import getLogger

from utils.config import Configuration


class Utils:
    def __init__(self, config: Configuration):
        self.logger = getLogger(__name__)
        self.logger.info("Initializing utils...")

        self.config = config

        self.interval = config.HEARTBEAT_FREQUENCY
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.running = False
        self.thread = None

    def start_heartbeat(self):
        self.logger.info("Initializing heartbeat...")
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_heartbeat)
            self.thread.start()

    def stop_heartbeat(self):
        if self.running:
            self.running = False
            self.thread.join()

    def _run_heartbeat(self):
        self.scheduler.enter(0, 1, self.heartbeat)
        while self.running:
            self.scheduler.run()

    def heartbeat(self):
        # Perform any necessary tasks or operations here

        # Log the heartbeat message
        self.logger.info("Heartbeat - Application is running")

        # Reschedule the heartbeat after the interval
        self.scheduler.enter(self.interval, 1, self.heartbeat)

    # def establish_exchange_connection(self):
    #     if self.config.TRAINING_WHEELS:
