import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def crate_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS survey_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    genre TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price FLOAT,
                    cover TEXT,
                    genre TEXT,
                    description TEXT,   -- Новое поле для описания блюда
                    category TEXT,      -- Новое поле для категории блюда
                    image_path TEXT     -- Новое поле для пути к картинке
                )
            """)
            conn.commit()

    def save_book(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    INSERT INTO books (name, price, cover, genre, description, category, image_path)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (data["name"], data["price"], data["cover"], data["genre"],
                 data["description"], data["category"], data["image_path"])
            )

    def get_all_books(self):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute("SELECT * from books")
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]
