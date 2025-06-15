
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import random
from pathlib import Path

DB_PATH = Path("flags.db")
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Сервер работает!"}

@app.get("/get-flag")
def get_flag():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT country, img FROM flags")
    all_flags = cur.fetchall()
    conn.close()

    # Выбираем случайный правильный флаг
    correct = random.choice(all_flags)
    country_correct, img_url = correct

    # Собираем три неправильных варианта
    wrong = random.sample([entry for entry in all_flags if entry != correct], 3)
    options = [country_correct] + [c for c, _ in wrong]
    random.shuffle(options)

    return {
        "img": img_url,
        "options": options,
        "answer": country_correct
    }