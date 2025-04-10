-- Käyttäjien taulu
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

-- Tuotteet-taulu
CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    descr TEXT,
    price INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    section_id INTEGER REFERENCES sections(id) ON DELETE CASCADE,
    condition_id INTEGER REFERENCES conditions(id) ON DELETE CASCADE
);

-- Tuote-luokat-taulu
CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

-- Osioiden taulu (kategorioiden nimilista)
CREATE TABLE sections (
    id INTEGER PRIMARY KEY,
    label TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE
);

-- Tila-taulu (tuotteen kunto)
CREATE TABLE conditions (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Viestit-taulu (keskustelut kahden käyttäjän välillä)
CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    item_id INTEGER REFERENCES items(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);