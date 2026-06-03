from abc import ABC, abstractmethod
import logging

class BaseWriter(ABC):
    def __init__(self):
        app_name = f"SmartFrame.{self.__class__.__name__}"
        self.logger = logging.getLogger(app_name)
        self.logger.info(f"New instance of {app_name}")

    @abstractmethod
    def write(self, data, path):
        pass