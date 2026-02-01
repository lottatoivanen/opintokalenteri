import db


def add_entry(title, description, date, user_id):
    sql = "INSERT INTO entries (title, description, date, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, date, user_id])

def get_entries():
    sql = "SELECT id, title, date FROM entries ORDER BY date ASC"
    return db.query(sql)