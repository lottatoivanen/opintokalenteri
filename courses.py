import db

def add_course(name, description, user_id):
    sql = """
    INSERT INTO courses (name, description, user_id) VALUES (?, ?, ?)
    """
    db.execute(sql, [name, description, user_id])

def get_course(course_id):
    sql = """
    SELECT courses.id, 
    courses.name, 
    courses.description, 
    courses.user_id, 
    users.username AS username 
    FROM courses 
    JOIN users ON users.id = courses.user_id 
    WHERE courses.id = ?
    """
    result = db.query(sql, [course_id])
    if result:
        return result[0]
    return None

def update_course(course_id, name, description):
    sql = """
    UPDATE courses SET name = ?, description = ? 
    WHERE id = ?
    """
    db.execute(sql, [name, description, course_id])

def delete_course_information(course_id):
    sql = """
    DELETE FROM comments WHERE course_id = ?
    """
    db.execute(sql, [course_id])
    sql = """
    DELETE FROM entries WHERE course_id = ?
    """
    db.execute(sql, [course_id])

def delete_course(course_id):
    delete_course_information(course_id)
    sql = """
    DELETE FROM courses WHERE id = ?
    """
    db.execute(sql, [course_id])