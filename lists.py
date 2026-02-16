import db

def get_items(q=""):
    base_sql = """
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
            i.sent_at
        FROM items i
        JOIN users u ON i.user_id = u.id
    """

    if q:
        sql = base_sql + """
            WHERE i.ttyype LIKE ?
               OR i.author LIKE ?
               OR i.title LIKE ?
               OR i.creator LIKE ?
               OR i.year LIKE ?
               OR i.condition LIKE ?
               OR i.content LIKE ?
        """
        pattern = f"%{q}%"
        params = [pattern] * 7
        return db.query(sql, params)

    return db.query(base_sql)



def add_item(ttyype, author, title, year, creator, condition, content, user_id):
    sql = """INSERT INTO items
             (ttyype, author, title, year, creator, condition, content, user_id)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
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
        return None  # tai nosta virhe, tai näytä 404
    return rows[0]


