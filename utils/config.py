import json
import logging

from enums.exchange import Exchange

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = "config/config.json"


class Configuration:
	def __init__(self):
		logger.info("Initialing config...")

		with open(CONFIG_FILE_PATH) as file:
			config_data = json.load(file)

		self.CURRENCY = config_data["currency"]

		self.HEARTBEAT_FREQUENCY = config_data["heartbeat_frequency"]

		self.TRAINING_WHEELS = config_data["training_wheels"]

		# Live exchange
		try:
			exchange_live = config_data["exchange"] if config_data["exchange"] != "" else None
		except: 
			exchange_live = None

		# Paper exchange
		try:
			exchange_paper = config_data["paper_exchange"] if config_data["paper_exchange"] != "" else None
		except: 
			exchange_paper = None

		self.EXCHANGE = self.get_trading_exchange(exchange_live, exchange_paper)

	def get_trading_exchange(self, live_exchange, paper_exchange):
		# TODO: add edge cases / validate
		# TODO: add default live trading exchange

		if self.TRAINING_WHEELS:
			# Paper trading
			if paper_exchange:
				return paper_exchange
			else:
				return Exchange.ALPACA
		else:
			# Live trading
			if live_exchange:
				return live_exchange
			else:
				return ""
