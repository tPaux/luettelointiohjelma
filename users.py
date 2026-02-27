import sqlite3
import db

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = """SELECT i.item_id,
                i.user_id,
                i.ttyype,
                i.author,
                i.title,
                i.creator,
                i.year,
                i.condition,
                i.content,
                i.sent_at
         FROM items i
         WHERE i.user_id = ?
         ORDER BY i.sent_at DESC"""

    return db.query(sql, [user_id])

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0]["image"] if result else None
