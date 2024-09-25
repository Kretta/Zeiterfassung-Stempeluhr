from functools import wraps

# Dekorator: Überprüft, ob die Einstempelung stattgefunden hat, bevor der Benutzer ausstempelt.
def check_einstempelung(func):
    @wraps(func)  # Beibehaltung der ursprünglichen Funktionseigenschaften.
    def wrapper(*args, **kwargs):
        # Zugriff auf die Instanz (self) über die Argumente der Funktion.
        instance = args[0]  
        
        # Überprüfen, ob der Benutzer eingestempelt ist.
        if instance.last_einstempel_time is None:
            # Falls nicht eingestempelt wurde, zeige eine Fehlermeldung und beende die Funktion.
            instance.main_window.info_dialog('Fehler', 'Sie müssen zuerst einstempeln!')
            return
        # Falls die Überprüfung bestanden wurde, die ursprüngliche Funktion ausführen.
        return func(*args, **kwargs)
    
    return wrapper
