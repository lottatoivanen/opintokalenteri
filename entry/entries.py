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
    sql = """SELECT entries.id, entries.title, entries.description, entries.date, users.username FROM entries, users WHERE entries.user_id = users.id AND entries.id = ?"""
    return db.query(sql, [entry_id])[0]
