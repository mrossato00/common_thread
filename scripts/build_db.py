import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "common_thread.db"
SCHEMA_PATH = ROOT / "db" / "schema.sql"
SEED_PATH = ROOT / "data" / "seed.json"


def main():
    # 1. Parti sempre da zero
    DB_PATH.unlink(missing_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    # 2. Crea le tabelle dallo schema
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    # 3. Leggi il JSON
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))

    work_ids = {}      # slug -> id numerico
    creator_ids = {}   # nome -> id numerico
    topic_ids = {}     # nome -> id numerico

    # 4. Inserisci le opere, con creators e topics
    for w in data["works"]:
        cur = conn.execute(
            "INSERT INTO works (slug, title, type, year) VALUES (?, ?, ?, ?)",
            (w["id"], w["title"], w["type"], w.get("year")),
        )
        work_id = cur.lastrowid
        work_ids[w["id"]] = work_id

        for name in w.get("creators", []):
            if name not in creator_ids:
                cur = conn.execute("INSERT INTO creators (name) VALUES (?)", (name,))
                creator_ids[name] = cur.lastrowid
            conn.execute(
                "INSERT INTO work_creators (work_id, creator_id) VALUES (?, ?)",
                (work_id, creator_ids[name]),
            )

        for name in w.get("topics", []):
            if name not in topic_ids:
                cur = conn.execute("INSERT INTO topics (name) VALUES (?)", (name,))
                topic_ids[name] = cur.lastrowid
            conn.execute(
                "INSERT INTO work_topics (work_id, topic_id) VALUES (?, ?)",
                (work_id, topic_ids[name]),
            )

    # (qui andranno le relazioni)

    conn.commit()

    # 5. Controllo di sanità
    for table in ["works", "creators", "topics", "work_creators", "work_topics", "relations"]:
        n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {n}")

    conn.close()


if __name__ == "__main__":
    main()