
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT,
    title TEXT,
    content TEXT,
    date DATETIME,
    authors TEXT,
    source TEXT,
    link TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS feed_sources (    
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    name TEXT,
    last_accessed DATETIME,
    last_etag TEXT
);