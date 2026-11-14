import sqlite3
from pathlib import Path
from flask import Flask, render_template, abort

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


@app.route("/work/<slug>")
def work(slug):
    conn = get_db()

    w = conn.execute(
        "SELECT id, slug, title, type, year FROM works WHERE slug = ?",
        (slug,),
    ).fetchone()

    if w is None:
        conn.close()
        abort(404)

    topics = conn.execute(
        """
        SELECT t.name
        FROM works w
        JOIN work_topics wt ON wt.work_id = w.id
        JOIN topics t ON t.id = wt.topic_id
        WHERE w.slug = ?
        """,
        (slug,),
    ).fetchall()

    relations = conn.execute(
        """
        SELECT s.title AS partenza, s.slug AS partenza_slug,
               r.type,
               tg.title AS arrivo, tg.slug AS arrivo_slug,
               r.explanation
        FROM relations r
        JOIN works s  ON s.id  = r.source_id
        JOIN works tg ON tg.id = r.target_id
        WHERE s.slug = ?
           OR tg.slug = ?
        """,
        (slug, slug),
    ).fetchall()

    conn.close()
    return render_template("work.html", work=w, topics=topics, relations=relations)


#tutte_le_opere_con_un_certo_titolo
@app.route("/topic/<name>")
def topic(name):
    """Pagina di un tema: tutte le opere che lo hanno (query 2)."""
    conn = get_db()

    works = conn.execute(
        """
        SELECT w.slug, w.title, w.type, w.year
        FROM works w
        JOIN work_topics wt ON wt.work_id = w.id
        JOIN topics t ON t.id = wt.topic_id
        WHERE t.name = ?
        ORDER BY w.year
        """,
        (name,),
    ).fetchall()

    conn.close()

    if not works:
        abort(404)

    return render_template("topic.html", name=name, works=works)