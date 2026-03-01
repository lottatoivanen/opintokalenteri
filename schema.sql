CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE entries (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    date DATE,
    user_id INTEGER REFERENCES users,
    course_id INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    comment TEXT,
    date DATE,
    user_id INTEGER REFERENCES users,
    entry_id INTEGER,
    course_id INTEGER,
    FOREIGN KEY(course_id) REFERENCES courses ON DELETE CASCADE,
    FOREIGN KEY(entry_id) REFERENCES entries(id) ON DELETE CASCADE
);

CREATE TABLE courses (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE entry_tags (
    id INTEGER PRIMARY KEY,
    entry_id INTEGER,
    title TEXT,
    value TEXT,
    FOREIGN KEY(entry_id) REFERENCES entries(id) ON DELETE CASCADE
);