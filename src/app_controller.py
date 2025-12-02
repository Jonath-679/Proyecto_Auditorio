from db_manager import DBManager


class AppController:
    def __init__(self):
        self.db = DBManager()

    # Metodos llamados desde la UI (main.py)