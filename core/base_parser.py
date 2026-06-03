from abc import ABC, abstractmethod
import logging

class BaseParcer(ABC):
    def __init__(self, config_dict):
        app_name = f"SmartFrame.{self.__class__.__name__}"
        self.logger = logging.getLogger(app_name)
        self.logger.info(f"New instance of {app_name}")

        self.config = config_dict
        self.raw_data = None

    @abstractmethod
    def parse(self):
        """Tramsform raw data to usefull data"""
        pass