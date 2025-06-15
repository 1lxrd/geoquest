from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

class ScoreEntry(BaseModel):
    name: str
    score: int

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

    correct = random.choice(all_flags)
    country_correct, img_url = correct
    wrong = random.sample([f for f in all_flags if f != correct], 3)
    options = [country_correct] + [c for c, _ in wrong]
    random.shuffle(options)

    return {"img": img_url, "options": options, "answer": country_correct}

@app.post("/submit-score")
def submit_score(entry: ScoreEntry):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO leaderboard(name, score) VALUES (?, ?)",
        (entry.name, entry.score)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/leaderboard")
def get_leaderboard():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT name, score FROM leaderboard ORDER BY score DESC, created_at ASC LIMIT 10"
    )
    rows = cur.fetchall()
    conn.close()
    return [{"name": name, "score": score} for name, score in rows]