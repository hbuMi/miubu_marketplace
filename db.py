import sqlite3
from flask import g, current_app
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    con = sqlite3.connect(current_app.config['DATABASE'])
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    g.db = con
    try:
        yield con
    finally:
        con.close()
        if 'db' in g:
            g.pop('db')

def execute(sql, params=(), commit=True):
    with get_db_connection() as con:
        try:
            result = con.execute(sql, params)
            if commit:
                con.commit()
            g.last_insert_id = result.lastrowid
            return result
        except sqlite3.Error as e:
            con.rollback()
            raise e

def query(sql, params=(), one=False):
    with get_db_connection() as con:
        cur = con.execute(sql, params)
        result = cur.fetchall()
        return result[0] if one and result else result

def executemany(sql, params_list):
    with get_db_connection() as con:
        try:
            result = con.executemany(sql, params_list)
            con.commit()
            return result
        except sqlite3.Error as e:
            con.rollback()
            raise e

def last_insert_id():
    return g.get('last_insert_id')

def save_blob(file_path, data):
    with get_db_connection() as con:
        try:
            with open(file_path, 'wb') as f:
                f.write(data)
            return True
        except Exception as e:
            raise e

@contextmanager
def transaction():
    with get_db_connection() as con:
        try:
            yield
            con.commit()
        except Exception:
            con.rollback()
            raise