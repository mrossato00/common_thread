def jaccard(a, b):
    """Similarità di Jaccard tra due insiemi: elementi in comune / elementi totali."""
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def similar_works(conn, slug, limit=5):
    """Opere più simili a `slug`, ordinate per similarità di Jaccard sui temi."""
    rows = conn.execute(
        """
        SELECT w.slug, w.title, t.name
        FROM works w
        JOIN work_topics wt ON wt.work_id = w.id
        JOIN topics t ON t.id = wt.topic_id
        """
    ).fetchall()

    topics_by_work = {}   # slug -> insieme dei suoi temi
    titles = {}           # slug -> titolo
    for r in rows:
        topics_by_work.setdefault(r["slug"], set()).add(r["name"])
        titles[r["slug"]] = r["title"]

    mine = topics_by_work.get(slug, set())

    scores = []
    for other, topics in topics_by_work.items():
        if other == slug:
            continue
        score = jaccard(mine, topics)
        if score > 0:
            scores.append((score, other))

    scores.sort(reverse=True)
    return [(other, titles[other], score) for score, other in scores[:limit]]