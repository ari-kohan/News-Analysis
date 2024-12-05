
CREATE TABLE IF NOT EXISTS news (
    uuid UUID PRIMARY KEY,
    title TEXT,
    summary TEXT,
    date TIMESTAMP,
    authors TEXT,
    source TEXT,
    link TEXT,
    people TEXT[],
    places TEXT[],
    agencies TEXT[],
    laws TEXT[],
    climate boolean,
);