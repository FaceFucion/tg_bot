import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def crate_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS opros_results(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    genre GENRE
                )
            """)
            conn.commit()

    def save_survey(self, data: dict):
        ...