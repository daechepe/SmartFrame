import json
import datetime
from pathlib import Path
import yaml
from icalendar import Calendar
from core.base_parcer import BaseParcer

class Parcer(BaseParcer):
    def __init__(self):
        self.current_path = Path(__file__).resolve().parent
        self.main_path = self.current_path.parents[1]

        config_path = self.current_path / "config.yaml"
    
        with open(config_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
        
        super().__init__(self.config)
        
        self.online = self.config.get("online_file")
        self.base_url = self.config.get("city_url")
        self.distrit = self.config.get("distritos")
        self.name = None
        self.format_parser = None
        self.events = None
        self.status = False
        
    def _ics_parser(self, path:Path) -> list:

        self.format_parser = "ics"
        parsed_events = []
        dt_today = datetime.date.today()
        with open(path, "r", encoding="utf-8") as f:
            try:
                cal = Calendar.from_ical(f.read())
                self.city = str(cal["X-WR-CALNAME"])

                for component in cal.walk():
                    if component.name == "VEVENT":
                        summary = component.get("SUMMARY")
                        summary = summary.to_ical().decode('utf-8') if hasattr(summary, 'to_ical') else str(
                            summary)

                        categories = component.get("CATEGORIES")
                        categories = categories.to_ical().decode('utf-8') if hasattr(categories, 'to_ical') else str(
                            categories)

                        event_type = categories if categories else summary

                        dtstart = component.get('DTSTART').dt
                        if type(dtstart) == datetime.datetime:
                            dtstart = dtstart.date()
                        days_left = (dtstart - dt_today).days
                        date_str = dtstart.strftime("%Y-%m-%d") if hasattr(dtstart, 'strftime') else str(dtstart)

                        parsed_events.append({
                            "summary": summary,
                            "categories": str(categories) if categories else None,
                            "date": date_str,
                            "days_left": days_left,
                            "type": event_type
                        })

                self.status = True
            except Exception as e:
                self.logger.error(f"[Error leyendo ICS {path.name}]: {e}")

            return parsed_events
    
    def _pdf_parser(self):
        self.format_parser = "pdf"
        pass
    
    def parse(self):
        raw_dir = self.main_path / "data" / "raw"
        processed_dir = self.main_path / "data" / "processed"

        if not raw_dir.exists():
            self.logger.info(f"[Parse]: La carpeta {raw_dir} no existe.")
            return

        for file_path in raw_dir.iterdir():
            if file_path.is_dir():
                continue

            if file_path.suffix.lower() == ".pdf":
                self.logger.info(f"[Parse]: PDF encontrado ({file_path.name}). Esta funcionalidad no está disponible.")
                continue

            if file_path.suffix.lower() == ".ics":
                self.logger.info(f"[Parse]: Procesando {file_path.name}...")
                self.events = self._ics_parser(file_path)

                if self.status:
                    processed_dir.mkdir(parents=True, exist_ok=True)
                    file_path.replace(processed_dir / file_path.name)
                break
    
    def save(self, output_path=None):
        if output_path is None:
            output_dir = self.main_path / "data" / "clean"
        else:
            output_dir = Path(output_path)

        if self.events and self.status:
            data_final = {
                "year": int(datetime.datetime.now().year),
                "last_update": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": self.format_parser,
                "name": self.city,
                "events": self.events
            }

            output_dir.mkdir(parents=True, exist_ok=True)
            file_to_save = output_dir / "GarbageCalendar.json"

            with open(file_to_save, "w", encoding="utf-8") as f:
                json.dump(data_final, f, ensure_ascii=False, indent=4)
            self.logger.info(f"[Save]: Datos guardados en {file_to_save}")
        else:
            self.logger.info(f"[Save]: No hay eventos para almacenar.")
    
if __name__ == "__main__":
    scrapper = Parcer()
    scrapper.parse()
