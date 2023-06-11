import json

from bottie import constants


class Configuration:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Configuration, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize your configuration attributes here
        self._load_config()
        # Add more configuration attributes as needed

    def _load_config(self):
        with open(constants.CONFIG_FILE_PATH) as file:
            self._config = json.load(file)
        file.close()

        with open(constants.CREDENTIALS_FILE_PATH) as file:
            self._credentials = json.load(file)
        file.close()

    # Dry run config
    def get_starting_funds(self):
        return self._config["paper_starting_balance"]

    # Operation config
    def is_paper_trading(self):
        return self._config["paper_trading"]

    def get_db_url(self):
        return self._config["db_url"]

    def get_initial_state(self):
        return self._config['initial_state']

    def reload_config(self):
        """
        Reload configuration files.
        """
        self._load_config()

    # API config
    def get_finnhub_credentials(self) -> list:
        _finnhub = self._credentials['finnhub']
        return {'api_key': _finnhub['api_key'], 'webhook_secret': _finnhub['webhook_secret']}


# def setup_logging_config(self):
#     self.
config = Configuration()
