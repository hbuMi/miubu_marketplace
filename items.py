import db

def add_item(title, descr, price, user_id):
    sql = """INSERT INTO items (title, descr, price, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, descr, price, user_id])