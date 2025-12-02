import sqlite3
from pathlib import Path


class DBManager:
    def __init__(self, path=None):
        if path is None:
            base_dir = Path.cwd() 
            path = base_dir / "storage" / "data" / "data"
        self.path = path #ruta a la bd
        self.conn = sqlite3.connect(path) #conexion a la bd
        self.create_tables()

    def create_tables(self):
        pass
    