import db

def add_entry(title, description, date, user_id):
    sql = """INSERT INTO entries (title, description, date, user_id) VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, date, user_id])

def get_entries(user_id):
    sql = """SELECT id, title, date FROM entries ORDER BY date ASC"""
    return db.query(sql)

def get_entries_by_user(user_id): 
    sql = """SELECT id, title, date FROM entries WHERE user_id = ? ORDER BY date ASC"""
    return db.query(sql, [user_id])

def get_entry(entry_id):
    sql = """SELECT entries.id, entries.title, entries.description, entries.date, entries.user_id, users.username AS username FROM entries JOIN users ON users.id = entries.user_id WHERE entries.id = ?"""
    result = db.query(sql, [entry_id])
    if result:
        return result[0]
    return None

def update_entry(entry_id, title, description, date):
    sql = """UPDATE entries SET title = ?, description = ?, date = ? WHERE id = ?"""
    db.execute(sql, [title, description, date, entry_id])

def delete_entry(entry_id):
    sql = """DELETE FROM entries WHERE id = ?"""
    db.execute(sql, [entry_id])

def find_entry(query):
    sql = """SELECT id, title, date FROM entries WHERE (title LIKE ? OR description LIKE ?) ORDER BY date ASC"""
    pattern = "%" + query + "%"
    return db.query(sql, [pattern, pattern])