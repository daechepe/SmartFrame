from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, config_dict):
        self.config = config_dict
        self.raw_data = None

    @abstractmethod
    def fetch(self):
        """Dowload raw data (HTML, PDF o ICS)"""
        pass

    @abstractmethod
    def parse(self):
        """Tramsform raw data to usefull data"""
        pass

    @abstractmethod
    def save(self, output_path):
        """Save procesed data on Json format"""
        pass