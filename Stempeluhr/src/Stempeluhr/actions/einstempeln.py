from datetime import datetime
from Stempeluhr.services.csv_handler import CSVHandler
from Stempeluhr.utils.time_utils import get_current_time_str, get_weekday_str

def einstempeln(csv_handler: CSVHandler, time_label, last_einstempel_time):
    current_time = datetime.now()
    time_str = get_current_time_str()
    weekday_str = get_weekday_str(current_time)
    time_label.text = f'Gestempelt um: {time_str} ({weekday_str})'
    csv_handler.save_to_csv('Einstempeln', time_str, weekday=weekday_str)
    return current_time
