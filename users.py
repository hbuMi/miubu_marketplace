from flask import session
import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = "SELECT id, username FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_items(user_id):
    sql = "SELECT id, title FROM items WHERE user_id = ? ORDER BY id DESC"
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_user_profile(user_id):
    sql = """SELECT 
                u.id, 
                u.username, 
                u.profile_pic, 
                u.bio, 
                u.location,
                u.created_at,
                (SELECT COUNT(*) FROM followers WHERE followed_id = u.id) AS follower_count,
                (SELECT COUNT(*) FROM followers WHERE follower_id = u.id) AS following_count,
                EXISTS(SELECT 1 FROM followers WHERE follower_id = ? AND followed_id = u.id) AS is_following
             FROM users u
             WHERE u.id = ?"""
    result = db.query(sql, [session.get('user_id', -1), user_id], one=True)
    if result:
        return dict(result)
    return None

def get_user_items(user_id):
    sql = """SELECT i.id, i.title, i.price, i.descr, s.label AS section, c.name AS condition
             FROM items i
             JOIN sections s ON i.section_id = s.id
             JOIN conditions c ON i.condition_id = c.id
             WHERE i.user_id = ?
             ORDER BY i.id DESC"""
    return db.query(sql, [user_id])

def follow_user(follower_id, followed_id):
    sql = "INSERT INTO followers (follower_id, followed_id) VALUES (?, ?)"
    db.execute(sql, [follower_id, followed_id])
    update_follower_count(followed_id)

def unfollow_user(follower_id, followed_id):
    sql = "DELETE FROM followers WHERE follower_id = ? AND followed_id = ?"
    db.execute(sql, [follower_id, followed_id])
    update_follower_count(followed_id)

def update_follower_count(user_id):
    sql = """UPDATE users
             SET follower_count = (SELECT COUNT(*) FROM followers WHERE followed_id = ?)
             WHERE id = ?"""
    db.execute(sql, [user_id, user_id])

def update_follow_stats(user_id):
    follower_count = get_follower_count(user_id)
    sql = "UPDATE users SET follower_count = ? WHERE id = ?"
    db.execute(sql, [follower_count, user_id])

def get_follower_count(user_id):
    sql = """SELECT COUNT(*) AS follower_count
             FROM followers
             WHERE followed_id = ?"""
    result = db.query(sql, [user_id], one=True)
    return result['follower_count'] if result else 0

def get_following_count(user_id):
    sql = """SELECT COUNT(*) AS following_count
             FROM followers
             WHERE follower_id = ?"""
    result = db.query(sql, [user_id], one=True)
    return result['following_count'] if result else 0

def update_profile(user_id, username, bio, location):
    sql = """UPDATE users 
             SET username = ?, bio = ?, location = ?
             WHERE id = ?"""
    db.execute(sql, [username, bio, location, user_id])

def update_profile_pic(user_id, filename):
    sql = "UPDATE users SET profile_pic = ? WHERE id = ?"
    db.execute(sql, [filename, user_id])

def verify_password(user_id, password):
    sql = "SELECT password_hash FROM users WHERE id = ?"
    user = db.query(sql, [user_id], one=True)
    return check_password_hash(user['password_hash'], password)

def update_password(user_id, new_password):
    hashed_pw = generate_password_hash(new_password)
    sql = "UPDATE users SET password = ? WHERE id = ?"
    db.execute(sql, [hashed_pw, user_id])