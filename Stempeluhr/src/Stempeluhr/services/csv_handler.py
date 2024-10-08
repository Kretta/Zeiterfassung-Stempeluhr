import csv
import os
from datetime import datetime, timedelta

# Der Pfad zur CSV-Datei, wo die Stempelzeiten gespeichert werden.
CSV_FILE = r'C:\Users\blue_\OneDrive\Dokumente\Python\Zeiterfassung\stempelzeiten.csv'

# Singleton-Metaklasse: Verhindert, dass mehrere Instanzen von CSVHandler erstellt werden.
class SingletonMeta(type):
    _instances = {}

    # __call__ wird aufgerufen, wenn eine Klasse instanziiert wird.
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

# Die CSVHandler-Klasse, die das Singleton-Pattern verwendet.
class CSVHandler(metaclass=SingletonMeta):
    def __init__(self, csv_file):
        self.csv_file = csv_file

    # Methode, um Daten in der CSV-Datei zu speichern.
    def save_to_csv(self, action, time, worked_time=None, weekly_hours=None, weekday=None):
        try:
            file_exists = os.path.isfile(self.csv_file)
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Falls die Datei neu erstellt wurde, die Header-Zeilen schreiben.
                if not file_exists:
                    writer.writerow(['Aktion', 'Zeit', 'Gearbeitete Zeit', 'Wochenstunden', 'Wochentag'])
                # Zeilen-Daten einfügen.
                row = [action, time, worked_time if worked_time else '', weekly_hours if weekly_hours else '', weekday if weekday else '']
                writer.writerow(row)
            print(f"Gespeichert: {action} um {time} ({weekday})")
        except Exception as e:
            print(f"Sorry, es ist ein Fehler beim Speichern der CSV-Datei aufgetreten: {e}")

    # Methode zur Berechnung der Wochenstunden basierend auf gespeicherten Zeiten.
    def calculate_weekly_hours(self):
        weekly_hours = timedelta()
        current_date = datetime.now().date()
        start_of_week = current_date - timedelta(days=current_date.weekday())

        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = datetime.strptime(row['Zeit'], "%Y-%m-%d %H:%M:%S").date()
                    if start_of_week <= date <= current_date and row['Gearbeitete Zeit']:
                        hours, minutes, seconds = map(int, row['Gearbeitete Zeit'].split(':'))
                        weekly_hours += timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except Exception as e:
            print(f"Fehler beim Berechnen der Wochenstunden: {e}")

        return weekly_hours
