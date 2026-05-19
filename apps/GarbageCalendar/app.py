import yaml

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)
    
class GarbageCalendar:
    def __init__(self) -> None:
        pass
    
    def update_data(self):
        # Lógica del scraper usando self.url
        pass

    def render(self):
        # Dibujar en el lienzo usando self.zona
        pass

print(config)