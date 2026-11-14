import sqlite3
from pathlib import Path
from flask import Flask, render_template

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "common_thread.db"

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@app.route("/")
def index():
    conn = get_db()
    works = conn.execute(
        "SELECT slug, title, type, year FROM works ORDER BY title"
    ).fetchall()
    conn.close()
    return render_template("index.html", works=works)