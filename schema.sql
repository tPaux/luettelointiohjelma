CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE lists (
    id INTEGER PRIMARY KEY,
    type TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    content TEXT,
    year INTEGER,
    title TEXT,
    creator TEXT,
    condition TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    list_id INTEGER REFERENCES lists
);