import json
import logging

logger = logging.getLogger(__name__)

CONFIG_FILE_PATH = 'config/config.json'

class Configuration:
	def __init__(self):
		logger.info("Initialing config...")
		
		with open(CONFIG_FILE_PATH) as file:
			config_data = json.load(file)
			
		self.CURRENCY = config_data["currency"]

		self.HEARTBEAT_FREQUENCY = config_data['heartbeat_frequency']

