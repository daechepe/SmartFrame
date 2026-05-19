from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, config_dict):
        self.config = config_dict
        self.raw_data = None

    @abstractmethod
    def fetch(self):
        """Descarga los datos crudos (HTML, PDF o ICS) desde la web"""
        pass

    @abstractmethod
    def parse(self):
        """Procesa los datos crudos y los convierte a un formato estándar"""
        pass

    @abstractmethod
    def save(self, output_path):
        """Guarda los datos procesados en el archivo JSON definitivo"""
        pass