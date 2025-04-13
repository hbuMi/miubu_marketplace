import db

def send_message(sender_id, receiver_id, item_id, content):
    sql = """INSERT INTO messages (sender_id, receiver_id, item_id, content) 
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [sender_id, receiver_id, item_id, content])

def get_conversations(user_id):
    sql = """WITH last_messages AS (
                SELECT 
                    item_id,
                    CASE WHEN sender_id = ? THEN receiver_id ELSE sender_id END AS partner_id,
                    MAX(timestamp) AS last_timestamp
                FROM messages
                WHERE sender_id = ? OR receiver_id = ?
                GROUP BY item_id, partner_id
            )
            SELECT 
                lm.partner_id,
                u.username AS partner_username,
                i.id AS item_id,
                i.title AS item_title,
                m.content AS last_message_content,
                m.timestamp AS last_message_timestamp,
                m.sender_id
            FROM last_messages lm
            JOIN messages m ON (
                m.timestamp = lm.last_timestamp AND
                m.item_id = lm.item_id AND
                (m.sender_id = ? OR m.receiver_id = ?)
            )
            JOIN users u ON u.id = lm.partner_id
            JOIN items i ON i.id = lm.item_id
            ORDER BY m.timestamp DESC"""
    
    return db.query(sql, [user_id, user_id, user_id, user_id, user_id])

def get_conversation(user_id, receiver_id, item_id):
    sql = """SELECT 
                m.id,
                m.content, 
                m.timestamp, 
                m.sender_id,
                u.username AS sender_username,
                i.title AS item_title
             FROM messages m
             JOIN users u ON u.id = m.sender_id
             JOIN items i ON i.id = m.item_id
             WHERE ((m.sender_id = ? AND m.receiver_id = ?) OR
                   (m.sender_id = ? AND m.receiver_id = ?))
             AND m.item_id = ?
             ORDER BY m.timestamp ASC"""
    
    messages = db.query(sql, [user_id, receiver_id, receiver_id, user_id, item_id])
    
    if not messages:
        return None
    
    other_user_sql = "SELECT id, username FROM users WHERE id = ?"
    other_user_result = db.query(other_user_sql, [receiver_id])
    other_user = other_user_result[0] if other_user_result else None
    
    return {
        "messages": messages,
        "other_user": other_user,
        "item": {"id": item_id, "title": messages[0]["item_title"]}
    }

def get_latest_item_id_for_conversation(user_id, receiver_id):
    sql = """SELECT item_id 
             FROM messages
             WHERE (sender_id = ? AND receiver_id = ?)
                OR (sender_id = ? AND receiver_id = ?)
             ORDER BY timestamp DESC
             LIMIT 1"""
    
    result = db.query(sql, [user_id, receiver_id, receiver_id, user_id])
    return result[0]["item_id"] if result else None