import db

def add_item(title, descr, price, user_id, section_id, condition_id):
    sql = """INSERT INTO items (title, descr, price, user_id, section_id, condition_id) VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [title, descr, price, user_id, section_id, condition_id])

def get_items():
    sql = "SELECT id, title FROM items ORDER BY id DESC"
    return db.query(sql)

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_sections():
    sql = "SELECT id, label, name FROM sections ORDER BY label, name"
    return db.query(sql)

def get_conditions():
    sql = "SELECT id, name FROM conditions ORDER BY id"
    return db.query(sql)

def get_section(section_id):
    sql = "SELECT id, label, name FROM sections WHERE id = ?"
    result = db.query(sql, [section_id])
    return result[0] if result else None

def get_condition(condition_id):
    sql = "SELECT id, name FROM conditions WHERE id = ?"
    result = db.query(sql, [condition_id])
    return result[0] if result else None

def get_item(item_id):
    sql = """SELECT items.id, items.title, items.descr, items.price, items.section_id, items.condition_id, 
             users.id user_id, users.username FROM items 
             JOIN users ON items.user_id = users.id WHERE items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, descr, price, section_id, condition_id):
    sql = """UPDATE items SET title = ?, descr = ?, price = ?, section_id = ?, condition_id = ? WHERE id = ?"""
    db.execute(sql, [title, descr, price, section_id, condition_id, item_id])

def remove_item(item_id):
    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])
    sql = "DELETE FROM items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title FROM items WHERE title like ? OR descr LIKE ? ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])