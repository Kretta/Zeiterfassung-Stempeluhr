from datetime import datetime

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
