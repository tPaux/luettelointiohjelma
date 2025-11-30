import db

def get_lists():
    sql = """SELECT l.id, l.title, COUNT(i.id) AS total, MAX(i.sent_at) AS last
            FROM lists l
            LEFT JOIN items i ON l.id = i.list_id  
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

def get_item(item_id):
    sql = "SELECT id, content, user_id, list_id FROM items WHERE id = ?"
    return db.query(sql, [item_id])[0]

def add_list(title, content, username):
    sql = "INSERT INTO lists (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, username])
    list_id = db.last_insert_id()
    add_item(content, username, list_id)
    return list_id

def add_item(content, username, list_id):
    sql = """INSERT INTO items (content, sent_at, user_id, list_id) VALUES
             (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, username, list_id])

def update_item(item_id, content):
    sql = "UPDATE items SET content = ? WHERE id = ?"
    db.execute(sql, [content, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])