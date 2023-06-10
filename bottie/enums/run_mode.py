from enum import Enum


class RunMode(Enum):
    """
    Bot running mode
    """

    LIVE = "live"
    PAPER = "paper"
    BACKTEST = "backtest"
    OTHER = "other"
