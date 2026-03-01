"""
test_db.py
Script for populating the database with big test data.
"""

import sqlite3
from datetime import datetime, timedelta
import random
import string

database_file = "database.db"

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_entries(num_entries=100):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    c.execute("SELECT id FROM users")
    users = [row[0] for row in c.fetchall()]

    c.execute("SELECT id FROM courses")
    courses = [row[0] for row in c.fetchall()]
    if not courses:
        courses = [None]

    for _ in range(num_entries):
        title = f"Entry {random_string(5)}"
        description = f"Description {random_string(20)}\nWith line break."
        date = (datetime.now() + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        user_id = random.choice(users)
        course_id = random.choice(courses)

        c.execute("""
            INSERT INTO entries (title, description, date, user_id, course_id)
            VALUES (?, ?, ?, ?, ?)
        """, (title, description, date, user_id, course_id))

        entry_id = c.lastrowid

        tag_title = random.choice(["tentti", "harjoitustyo", "kotitehtava"])
        tag_value = f"Value {random_string(3)}"
        c.execute("""
            INSERT INTO entry_tags (entry_id, title, value)
            VALUES (?, ?, ?)
        """, (entry_id, tag_title, tag_value))

    conn.commit()
    conn.close()
    print(f"{num_entries} entries added successfully.")

def create_courses(num_courses=200):
    conn = sqlite3.connect(database_file)
    c = conn.cursor()

    c.execute("SELECT id FROM users")
    users = [row[0] for row in c.fetchall()]

    for _ in range(num_courses):
        name = f"Course {random_string(6)}"
        description = f"Description {random_string(20)}"
        user_id = random.choice(users)

        c.execute("""
            INSERT INTO courses (name, description, user_id)
            VALUES (?, ?, ?)
        """, (name, description, user_id))

    conn.commit()
    conn.close()
    print(f"{num_courses} courses added successfully.")


if __name__ == "__main__":
    create_entries(200)
    create_courses(200)