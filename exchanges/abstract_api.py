from abc import ABC, abstractmethod


class ExchangeInterface(ABC):
    @abstractmethod
    def establish_connection(
        self, api_key: str, api_secret: str, training_wheels: bool
    ):
        pass
