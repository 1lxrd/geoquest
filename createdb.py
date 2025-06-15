import sqlite3
from pathlib import Path
import requests

DB_PATH = Path("flags.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS flags (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT    NOT NULL,
            img     TEXT    NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leaderboard (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            score       INTEGER NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cur.execute("SELECT COUNT(*) FROM flags")
    if cur.fetchone()[0] == 0:
        url = "https://restcountries.com/v3.1/all?fields=name,cca2"
        response = requests.get(url)
        response.raise_for_status()
        for c in response.json():
            name = c.get("name", {}).get("common")
            code = c.get("cca2", "").lower()
            if not name or not code:
                continue
            img_url = f"https://flagcdn.com/w320/{code}.png"
            cur.execute(
                "INSERT INTO flags(country, img) VALUES (?, ?)",
                (name, img_url)
            )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"БД '{DB_PATH}' инициализирована.")