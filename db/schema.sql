PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS relations;
DROP TABLE IF EXISTS work_creators;
DROP TABLE IF EXISTS work_topics;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS works;

CREATE TABLE works (
    id      INTEGER PRIMARY KEY,
    slug    TEXT NOT NULL UNIQUE,
    title   TEXT NOT NULL,
    type    TEXT NOT NULL CHECK (type IN ('book','film','game','music')),
    year    INTEGER,
    summary TEXT
);
CREATE TABLE topics (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE creators (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE work_topics (
    work_id  INTEGER NOT NULL REFERENCES works(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    PRIMARY KEY (work_id, topic_id)
);
CREATE TABLE work_creators (
    work_id    INTEGER NOT NULL REFERENCES works(id),
    creator_id INTEGER NOT NULL REFERENCES creators(id),
    role       TEXT,
    PRIMARY KEY (work_id, creator_id)
);
CREATE TABLE relations (
    id          INTEGER PRIMARY KEY,
    source_id   INTEGER NOT NULL REFERENCES works(id),
    target_id   INTEGER NOT NULL REFERENCES works(id),
    type        TEXT NOT NULL,
    explanation TEXT NOT NULL,
    CHECK (source_id != target_id)
);