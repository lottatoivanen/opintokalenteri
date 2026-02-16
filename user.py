import db

def get_user_by_username(username):
    sql = """SELECT id, username FROM users WHERE username = ?"""
    result = db.query(sql, [username])
    if result:
        return result[0]
    return None