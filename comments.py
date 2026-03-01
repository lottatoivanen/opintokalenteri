import db
import datetime

def add_comment_entry(entry_id, user_id, comment):
    sql = """
    INSERT INTO comments (entry_id, user_id, comment, date) VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [entry_id, user_id, comment, datetime.date.today()])

def add_comment_course(course_id, user_id, comment):
    sql = """
    INSERT INTO comments (course_id, user_id, comment, date) VALUES (?, ?, ?, ?)
    """
    db.execute(sql, [course_id, user_id, comment, datetime.date.today()])

def get_comments_entry(entry_id):
    sql = """
    SELECT comments.id, 
    comments.comment, 
    comments.user_id, 
    comments.entry_id, 
    users.username, 
    comments.date 
    FROM comments 
    JOIN users ON users.id = comments.user_id 
    WHERE comments.entry_id = ? 
    """
    return db.query(sql, [entry_id])

def get_comments_course(course_id):
    sql = """
    SELECT comments.id, 
    comments.comment, 
    comments.user_id, 
    comments.course_id, 
    users.username, 
    comments.date 
    FROM comments 
    JOIN users ON users.id = comments.user_id 
    WHERE comments.course_id = ?
    """
    return db.query(sql, [course_id])

def get_comment(comment_id):
    sql = """
    SELECT comments.id, 
    comments.comment, 
    comments.user_id, 
    comments.course_id, 
    comments.entry_id, 
    users.username, 
    comments.date 
    FROM comments 
    JOIN users ON users.id = comments.user_id 
    WHERE comments.id = ?
    """
    result = db.query(sql, [comment_id])
    if result:
        return result[0]
    return None

def delete_comment(comment_id):
    sql = """
    DELETE FROM comments WHERE id = ?
    """
    db.execute(sql, [comment_id])