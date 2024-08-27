from datetime import datetime
from Stempeluhr.services.csv_handler import CSVHandler
from Stempeluhr.utils.time_utils import get_current_time_str, get_weekday_str, format_timedelta

def ausstempeln(csv_handler: CSVHandler, time_label, worked_time_label, weekly_hours_label, last_einstempel_time, main_window):
    current_time = datetime.now()
    time_str = get_current_time_str()
    weekday_str = get_weekday_str(current_time)
    time_label.text = f'Abgestempelt um: {time_str} ({weekday_str})'

    if last_einstempel_time:
        worked_time = current_time - last_einstempel_time
        worked_time_str = format_timedelta(worked_time)
        worked_time_label.text = f'Gearbeitete Zeit: {worked_time_str}'
        
        weekly_hours = None
        if current_time.weekday() == 4:  # Freitag
            weekly_hours = csv_handler.calculate_weekly_hours()
            weekly_hours_str = format_timedelta(weekly_hours)
            weekly_hours_label.text = f'Wochenstunden: {weekly_hours_str}'
            main_window.info_dialog('Wochenstunden', f'Die Gesamtarbeitszeit dieser Woche beträgt: {weekly_hours_str}')
        
        csv_handler.save_to_csv('Ausstempeln', time_str, worked_time_str, weekly_hours_str if weekly_hours else None, weekday=weekday_str)
        last_einstempel_time = None
    else:
        worked_time_label.text = 'Gearbeitete Zeit: Nicht verfügbar'
        csv_handler.save_to_csv('Ausstempeln', time_str, weekday=weekday_str)
