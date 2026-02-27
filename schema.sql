CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);


CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    ttyype TEXT,
    content TEXT,
    year INTEGER,
    title TEXT,
    creator TEXT,
    author TEXT,
    condition TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    image BLOB

);

CREATE INDEX idx_items ON items (item_id);

/
