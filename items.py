import db

def add_item(title, descr, price, user_id):
    sql = """INSERT INTO items (title, descr, price, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, descr, price, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = "SELECT items.id, items.title, items.descr, items.price, users.id user_id, users.username FROM items, users WHERE items.user_id = users.id AND items.id = ?"
    return db.query(sql, [item_id])[0]

def update_item(item_id, title, descr, price):
    sql = """UPDATE items SET title = ?, descr = ?, price = ? WHERE id = ?"""
    db.execute(sql, [title, descr, price, item_id])