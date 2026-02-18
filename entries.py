import db

def add_entry(title, description, date, user_id, course_id):
    sql = """INSERT INTO entries (title, description, date, user_id, course_id) VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [title, description, date, user_id, course_id])

def get_entry(entry_id):
    sql = """SELECT entries.id, entries.title, entries.description, entries.date, entries.user_id, courses.id AS course_id, courses.name AS course_name, users.username AS username FROM entries JOIN users ON users.id = entries.user_id LEFT JOIN courses ON courses.id = entries.course_id WHERE entries.id = ?"""
    result = db.query(sql, [entry_id])
    if result:
        return result[0]
    return None

def get_entries_by_course(course_id):
    sql = """SELECT entries.id, entries.title, entries.description, entries.date, entries.user_id, courses.id AS course_id, courses.name AS course_name FROM entries LEFT JOIN courses ON courses.id = entries.course_id WHERE entries.course_id = ? ORDER BY entries.date ASC"""
    return db.query(sql, [course_id])

def update_entry(entry_id, title, description, date, course_id):
    sql = """UPDATE entries SET title = ?, description = ?, date = ?, course_id = ? WHERE id = ?"""
    db.execute(sql, [title, description, date, course_id, entry_id])

def delete_entry(entry_id):
    sql = """DELETE FROM entries WHERE id = ?"""
    db.execute(sql, [entry_id])

def find_entry(query):
    sql = """SELECT id, title, date FROM entries WHERE (title LIKE ? OR description LIKE ?) ORDER BY date ASC"""
    pattern = "%" + query + "%"
    return db.query(sql, [pattern, pattern])