import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from datetime import datetime
from Stempeluhr.services.csv_handler import CSVHandler

CSV_FILE = r'C:\Users\blue_\OneDrive\Dokumente\Python\Zeiterfassung\stempelzeiten.csv'
DEUTSCHE_WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

def get_current_time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_weekday_str(date):
    return DEUTSCHE_WOCHENTAGE[date.weekday()]

def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

class Stempeluhr(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_handler = CSVHandler(CSV_FILE)

    def startup(self):
        """Construct and show the Toga application."""
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        self.time_label = toga.Label('Keine Stempelzeit', style=Pack(padding=5))
        self.worked_time_label = toga.Label('Gearbeitete Zeit: 00:00:00', style=Pack(padding=5))
        self.weekly_hours_label = toga.Label('Wochenstunden: 00:00:00', style=Pack(padding=5))

        self.einstempeln_button = toga.Button('Einstempeln', on_press=self.einstempeln, style=Pack(padding=5))
        self.ausstempeln_button = toga.Button('Ausstempeln', on_press=self.ausstempeln, style=Pack(padding=5))

        button_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button_box.add(self.einstempeln_button)
        button_box.add(self.ausstempeln_button)

        main_box.add(self.time_label)
        main_box.add(self.worked_time_label)
        main_box.add(self.weekly_hours_label)
        main_box.add(button_box)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        self.last_einstempel_time = None

    def einstempeln(self, widget):
        current_time = datetime.now()
        self.last_einstempel_time = current_time
        time_str = get_current_time_str()
        weekday_str = get_weekday_str(current_time)
        self.time_label.text = f'Gestempelt um: {time_str} ({weekday_str})'
        self.csv_handler.save_to_csv('Einstempeln', time_str, weekday=weekday_str)

    def ausstempeln(self, widget):
        current_time = datetime.now()
        time_str = get_current_time_str()
        weekday_str = get_weekday_str(current_time)
        self.time_label.text = f'Abgestempelt um: {time_str} ({weekday_str})'

        if self.last_einstempel_time:
            worked_time = current_time - self.last_einstempel_time
            worked_time_str = format_timedelta(worked_time)
            self.worked_time_label.text = f'Gearbeitete Zeit: {worked_time_str}'
            
            weekly_hours = None
            if current_time.weekday() == 4:  # Freitag
                weekly_hours = self.csv_handler.calculate_weekly_hours()
                weekly_hours_str = format_timedelta(weekly_hours)
                self.weekly_hours_label.text = f'Wochenstunden: {weekly_hours_str}'
                self.main_window.info_dialog('Wochenstunden', f'Die Gesamtarbeitszeit dieser Woche beträgt: {weekly_hours_str}')
            
            self.csv_handler.save_to_csv('Ausstempeln', time_str, worked_time_str, weekly_hours_str if weekly_hours else None, weekday=weekday_str)
            self.last_einstempel_time = None
        else:
            self.worked_time_label.text = 'Gearbeitete Zeit: Nicht verfügbar'
            self.csv_handler.save_to_csv('Ausstempeln', time_str, weekday=weekday_str)

def main():
    return Stempeluhr()
