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

CREATE INDEX IF NOT EXISTS idx_items_user_id ON items(user_id);
CREATE INDEX IF NOT EXISTS idx_items_item_id ON items(item_id);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);




/
