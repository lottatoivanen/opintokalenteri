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
    course_id INTEGER REFERENCES courses
    
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
    FOREIGN KEY(entry_id) INTEGER REFERENCES entries(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);