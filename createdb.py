# create_db.py
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
    cur.execute("SELECT COUNT(*) FROM flags")
    if cur.fetchone()[0] == 0:

        url = "https://restcountries.com/v3.1/all?fields=name,cca2"
        response = requests.get(url)
        response.raise_for_status()
        countries = response.json()
        for country in countries:
            name = country.get("name", {}).get("common")
            code = country.get("cca2", "").lower()
            if not name or not code:
                continue
            img_url = f"https://flagcdn.com/w320/{code}.png"
            cur.execute(
                "INSERT INTO flags (country, img) VALUES (?, ?)",
                (name, img_url)
            )
        conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database '{DB_PATH}' initialized and populated with flags of all countries.")