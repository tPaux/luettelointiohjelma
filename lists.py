import db

def get_lists():
    sql = """SELECT l.id, l.title, COUNT(i.id) AS total, MAX(i.sent_at) AS last
            FROM lists l
            LEFT JOIN items i ON l.id = i.list_id  -- Käytetään LEFT JOIN:ia, jotta saadaan myös tyhjät listat
            GROUP BY l.id
            ORDER BY l.id DESC"""
    return db.query(sql)

def get_list(list_id):
    sql = "SELECT id, title FROM lists WHERE id = ?"
    return db.query(sql, [list_id])[0]

def get_items(list_id):
    sql = """SELECT i.id, i.content, i.sent_at, i.user_id, u.username
             FROM items m, users u
             WHERE i.user_id = u.id AND i.list_id = ?
             ORDER BY i.id"""
    return db.query(sql, [list_id])

def get_message(message_id):
    sql = "SELECT id, content, user_id, list_id FROM items WHERE id = ?"
    return db.query(sql, [message_id])[0]

def add_list(title, content, user_id):
    sql = "INSERT INTO lists (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])
    list_id = db.last_insert_id()
    add_message(content, user_id, list_id)
    return list_id

def add_message(content, user_id, list_id):
    sql = """INSERT INTO items (content, sent_at, user_id, list_id) VALUES
             (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, list_id])

def update_message(message_id, content):
    sql = "UPDATE items SET content = ? WHERE id = ?"
    db.execute(sql, [content, message_id])

def remove_message(message_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [message_id])