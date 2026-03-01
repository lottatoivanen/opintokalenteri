"""
user.py
Functions for handling user information in the application.
"""

from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user_by_username(username):
    sql = """
    SELECT id, username FROM users WHERE username = ?
    """
    result = db.query(sql, [username])
    if result:
        return result[0]
    return None

def get_entries_by_user(user_id):
    sql = """
    SELECT entries.id,
    entries.title,
    entries.date,
    courses.id AS course_id,
    courses.name AS course_name
    FROM entries
    LEFT JOIN courses ON courses.id = entries.course_id
    WHERE entries.user_id = ?
    ORDER BY date ASC
    """
    return db.query(sql, [user_id])

def get_courses_by_user(user_id):
    sql = """
    SELECT id, name FROM courses WHERE user_id = ?
    """
    return db.query(sql, [user_id])

def get_all_courses_except_user(user_id):
    sql = """
    SELECT courses.id,
    courses.name,
    courses.description,
    courses.user_id,
    users.username AS username
    FROM courses
    JOIN users ON users.id = courses.user_id
    WHERE courses.user_id != ?
    """
    return db.query(sql, [user_id])

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = """
    INSERT INTO users (username, password_hash) VALUES (?, ?)
    """
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = """
    SELECT id, password_hash FROM users WHERE username = ?
    """
    result = db.query(sql, [username])
    if not result:
        return False
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return False
