CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    descr TEXT,
    price INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    section_id INTEGER REFERENCES sections(id) ON DELETE CASCADE,
    condition_id INTEGER REFERENCES conditions(id) ON DELETE CASCADE
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

CREATE TABLE sections (
    id INTEGER PRIMARY KEY,
    label TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE conditions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);