import os
import json
import datetime
import glob
import yaml
import requests
from core.base_scrapper import BaseScraper

class Scrapper(BaseScraper):
    def __init__(self):
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_path, "config.yaml")
    
        with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        
        super().__init__(self.config)
        
        self.online = self.config.get("online_file")
        self.base_url = self.config.get("city_url")
        self.distrito = self.config.get("distritos")
        self.name = None
        self.format_parser = None
        self.events = None
        
    def __ics_parser__(self, path) -> list:
        raw_file = open(path)
        self.format_parser = "ics"
        events = []
        while True:
            line = raw_file.readline()
            line = line.rstrip('\n\r')
            sep = line.find(":")
            key = line[:sep]
            value = line[sep+1:]
            
            if line.startswith("BEGIN:VEVENT"):
                current_event = {}
            elif key.lower().startswith("summary"):
                current_event["summary"] = value
            elif key.lower().startswith("categories"):
                current_event["categories"] = value
            elif key.lower().startswith("dtstart;"):
                fecha_formateada = f"{value[0:4]}-{value[4:6]}-{value[6:8]}"
                current_event["date"] = fecha_formateada
            elif line.startswith("END:VEVENT"):
                if "categories" in current_event:
                    current_event["type"] = current_event["categories"]
                else:
                    current_event["type"] = current_event["summary"]
                if "date" in current_event and "type" in current_event:
                    events.append(current_event)
            elif line.startswith("X-WR-CALNAME:"):
                self.city = value
                
            if line == 'END:VCALENDAR':
                break
        
        raw_file.close()
        return events
    
    def __pdf_parser__(self):
        self.format_parser = "pdf"
        pass
    
    def fetch(self):
        try:
            session = requests.Session()
            session.headers.update({"User-Agent": "SmartFrame-Agent/1.0"})
        except Exception as e:
            print(f"[Error Crítico en Scraper]: {e}")
            return False
    
    def parse(self):
        current_path = os.path.dirname(os.path.abspath(__name__))
        data_path = os.path.join(current_path, "data/raw")
        
        os.chdir(data_path)
        raw_files = glob.glob("*.*")
        
        for f in raw_files:
            if "pdf" in f:
                print("Actualmente esta funcionalidad no esta disponible")
                break
            elif "ics" in f:
                self.events = self.__ics_parser__(data_path + "/" + f)
                if not os.path.exists(current_path + "/data/procesed"):
                    os.makedirs(current_path + "/data/procesed")
                os.rename(data_path + "/" + f, current_path + "/data/procesed/" + f)
                break
    
    def save(self, output_path=None):
        os.chdir("..")
        current_path = os.path.dirname(os.path.abspath(__name__))
        output_path = os.path.join(current_path, "clean")
        
        if self.events:
            data_final = {
                "año": int(datetime.datetime.now().year),
                "ultima_actualizacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": self.format_parser,
                "name": self.city,
                "eventos": self.events
            }
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                
            with open(output_path + "/GarbageCalendar.json", "w", encoding="utf-8") as f:
                json.dump(data_final, f, ensure_ascii=False, indent=4)
        else:
            print("No hay eventos para almacenar")
    
if __name__ == "__main__":
    x = Scrapper()
    x.parse()
    x.save()
