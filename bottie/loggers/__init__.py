import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler, SysLogHandler

from bottie.configuration.configuration import config

from bottie import constants

from bottie.loggers.buffer_handler import BufferHandler
from bottie.loggers.set_log_levels import set_loggers
from bottie.loggers.std_err_stream_handler import StdErrStreamHandler


logger = logging.getLogger(__name__)
LOGFORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Initialize bufferhandler - will be used for /log endpoints
bufferHandler = BufferHandler(1000)
bufferHandler.setFormatter(Formatter(LOGFORMAT))


def get_existing_handlers(handlertype):
    """
    Returns Existing handler or None (if the handler has not yet been added to the root handlers).
    """
    return next((h for h in logging.root.handlers if isinstance(h, handlertype)), None)


def setup_logging() -> None:
    """
    Uses INFO loglevel and only the Streamhandler.
    Early messages (before proper logging setup) will therefore only be sent to additional
    logging handlers after the real initialization, because we don't know which
    ones the user desires beforehand.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[StdErrStreamHandler()],
    )

    # Create a file handler for the log file
    file_handler = RotatingFileHandler(
        constants.LOGS_PATH, maxBytes=1024 * 1024 * 10, backupCount=10
    )  # 10Mb
    file_handler.setFormatter(Formatter(log_format))

    # Add the file handler to the root logger
    logging.root.addHandler(file_handler)

    # def setup_logging(config: config) -> None:
    #     """
    #     Process -v/--verbose, --logfile options
    #     """
    #     # Log level
    #     verbosity = config["verbosity"]
    #     logging.root.addHandler(bufferHandler)

    #     logfile = config.get("logfile")

    #     if logfile:
    #         s = logfile.split(":")
    #         if s[0] == "syslog":
    #             # Address can be either a string (socket filename) for Unix domain socket or
    #             # a tuple (hostname, port) for UDP socket.
    #             # Address can be omitted (i.e. simple 'syslog' used as the value of
    #             # config['logfilename']), which defaults to '/dev/log', applicable for most
    #             # of the systems.
    #             address = (
    #                 (s[1], int(s[2])) if len(s) > 2 else s[1] if len(s) > 1 else "/dev/log"
    #             )
    #             handler_sl = get_existing_handlers(SysLogHandler)
    #             if handler_sl:
    #                 logging.root.removeHandler(handler_sl)
    #             handler_sl = SysLogHandler(address=address)
    #             # No datetime field for logging into syslog, to allow syslog
    #             # to perform reduction of repeating messages if this is set in the
    #             # syslog config. The messages should be equal for this.
    #             handler_sl.setFormatter(Formatter("%(name)s - %(levelname)s - %(message)s"))
    #             logging.root.addHandler(handler_sl)
    #         else:
    #             handler_rf = get_existing_handlers(RotatingFileHandler)
    #             if handler_rf:
    #                 logging.root.removeHandler(handler_rf)
    #             handler_rf = RotatingFileHandler(
    #                 logfile, maxBytes=1024 * 1024 * 10, backupCount=10  # 10Mb
    #             )
    #             handler_rf.setFormatter(Formatter(LOGFORMAT))
    #             logging.root.addHandler(handler_rf)

    #     logging.root.setLevel(logging.INFO if verbosity < 1 else logging.DEBUG)
    #     set_loggers(verbosity)

    # logger.info("Verbosity set to %s", verbosity)
