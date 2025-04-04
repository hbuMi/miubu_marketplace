import db

def add_item(title, descr, price, user_id):
    sql = """INSERT INTO items (title, descr, price, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, descr, price, user_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = "SELECT items.id, items.title, items.descr, items.price, users.id user_id, users.username FROM items JOIN users ON items.user_id = users.id WHERE items.id = ?"
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, descr, price):
    sql = """UPDATE items SET title = ?, descr = ?, price = ? WHERE id = ?"""
    db.execute(sql, [title, descr, price, item_id])

def remove_item(item_id):
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title FROM items WHERE title like ? OR descr LIKE ? ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])