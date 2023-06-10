#!/usr/bin/env python3
"""
Main Freqtrade bot script.
Read the documentation to know what cli arguments you need.
"""
import logging
import sys
from typing import Any, List, Optional

from bottie.utils.gc_setup import gc_set_threshold


# check min. python version
if sys.version_info < (3, 8):  # pragma: no cover
    sys.exit("Bottie requires Python version >= 3.8")

from bottie import __version__
from bottie.loggers import setup_logging

from bottie.bottie import Bottie

logger = logging.getLogger("bottie")


def main() -> None:
    return_code: Any = 1
    try:
        setup_logging()

        logger.info(f"bottie {__version__}")
        gc_set_threshold()

        bottie = Bottie()
    except SystemExit as e:  # pragma: no cover
        return_code = e
    except KeyboardInterrupt:
        logger.info("SIGINT received, aborting ...")
        return_code = 0
    except Exception as e:
        logger.error(str(e))
        return_code = 2
    except Exception:
        logger.exception("Fatal exception!")
    finally:
        sys.exit(return_code)


if __name__ == "__main__":  # pragma: no cover
    main()
