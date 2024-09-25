import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from Stempeluhr.services.csv_handler import CSVHandler  # Singleton CSVHandler
from Stempeluhr.actions.einstempeln import einstempeln
from Stempeluhr.actions.ausstempeln import ausstempeln
from Stempeluhr.utils.decorators import check_einstempelung  # Import des Dekorators

CSV_FILE = r'C:\Users\blue_\OneDrive\Dokumente\Python\Zeiterfassung\stempelzeiten.csv'

class Stempeluhr(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # CSVHandler wird nur einmal erstellt, dank Singleton-Pattern
        self.csv_handler = CSVHandler(CSV_FILE)
        self.last_einstempel_time = None

    def startup(self):
        """Erstellt und zeigt die Toga-Anwendung."""
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Anzeige der Zeit und Arbeitsstunden
        self.time_label = toga.Label('Keine Stempelzeit', style=Pack(padding=5))
        self.worked_time_label = toga.Label('Gearbeitete Zeit: 00:00:00', style=Pack(padding=5))
        self.weekly_hours_label = toga.Label('Wochenstunden: 00:00:00', style=Pack(padding=5))

        # Einstempel- und Ausstempel-Schaltflächen
        self.einstempeln_button = toga.Button('Einstempeln', on_press=self.einstempeln, style=Pack(padding=5))
        self.ausstempeln_button = toga.Button('Ausstempeln', on_press=self.ausstempeln, style=Pack(padding=5))

        button_box = toga.Box(style=Pack(direction=ROW, padding=5))
        button_box.add(self.einstempeln_button)
        button_box.add(self.ausstempeln_button)

        main_box.add(self.time_label)
        main_box.add(self.worked_time_label)
        main_box.add(self.weekly_hours_label)
        main_box.add(button_box)

        # Hauptfenster anzeigen
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    # Einstempelfunktion
    def einstempeln(self, widget):
        # Einstempeln führt die Einstempel-Aktion durch
        self.last_einstempel_time = einstempeln(self.csv_handler, self.time_label, self.last_einstempel_time)

    @check_einstempelung  # Der Dekorator überprüft, ob eingestempelt wurde.
    def ausstempeln(self, widget):
        # Ausstempeln führt die Ausstempel-Aktion durch
        ausstempeln(self.csv_handler, self.time_label, self.worked_time_label, self.weekly_hours_label, self.last_einstempel_time, self.main_window)

def main():
    return Stempeluhr()
