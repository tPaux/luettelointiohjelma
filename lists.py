import db

def get_items(page, page_size):
    sql = """
        SELECT DISTINCT
            i.item_id,
            u.username,
            i.ttyype,
            i.author,
            i.title,
            i.creator,
            i.year,
            i.condition,
            i.content,
            i.sent_at,
            i.user_id
        FROM items i
        JOIN users u ON i.user_id = u.id
        LIMIT ? OFFSET ?
    """

    limit = page_size
    offset = page_size * (page - 1)
    result = db.query(sql, [limit, offset])
    return result if result else []

def search(q):
    sql = """
        SELECT DISTINCT
            i.item_id,
            u.username,
            i.ttyype,
            i.author,
            i.title,
            i.creator,
            i.year,
            i.condition,
            i.content,
            i.sent_at,
            i.user_id
        FROM items i
        JOIN users u ON i.user_id = u.id
        WHERE i.ttyype LIKE ?
            OR i.author LIKE ?
            OR i.title LIKE ?
            OR i.creator LIKE ?
            OR i.year LIKE ?
            OR i.condition LIKE ?
            OR i.content LIKE ?
        """
    pattern = "%" + q + "%"
    return db.query(sql, [pattern] * 7)



def add_item(ttyype, author, title, year, creator, condition, content, user_id):
    sql = """INSERT INTO items
             (ttyype, author, title, year, creator, condition, content, user_id, sent_at)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))"""
    return db.execute(sql, [ttyype, author, title, year, creator, condition, content, user_id])


def get_item(item_id):
    sql = """
    SELECT u.id,
           i.item_id,
           i.ttyype,
           i.author,
           i.title,
           i.year,
           i.creator,
           i.condition,
           i.content,
           u.username,
           i.sent_at,
           i.user_id
    FROM items i
    JOIN users u ON i.user_id = u.id
    WHERE i.item_id = ?
    """
    rows = db.query(sql, [item_id])
    if not rows:
        return None
    return rows[0]

def update_item(item_id, ttyype, author, title, year, creator, condition, content):
    sql="UPDATE items SET content = ?, ttyype = ?, author = ?, title = ?, year = ?, creator = ?, condition = ? WHERE item_id = ?"
    db.execute(sql, [content, ttyype, author, title, year, creator, condition, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE item_id = ?"
    db.execute(sql, [item_id])

def items_count():
    sql = "SELECT COUNT(*) FROM items"
    result = db.query(sql)
    return result[0][0]

def search_count(q):
    pattern = f"%{q}%"

    cols = db.query("PRAGMA table_info(items)")
    allowed_cols = {"ttyype", "author", "title", "creator", "year", "condition", "content"}
    col_names = [c[1] for c in cols if c[1] in allowed_cols]
    if not col_names:
        return 0


    where = " OR ".join([f"{col} LIKE ?" for col in col_names])
    params = [pattern] * len(col_names)

    sql = f"SELECT COUNT(*) AS cnt FROM items WHERE {where}"
    result = db.query(sql, params)

    return result[0]["cnt"]




