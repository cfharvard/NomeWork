-- SQLite
-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user TEXT NOT NULL,
--     hash TEXT NOT NULL
-- );

-- CREATE TABLE classes (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL,
--     user_id INTEGER NOT NULL,
--     FOREIGN KEY (user_id) REFERENCES users (id)
-- );

-- CREATE TABLE times (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     class_id INTEGER NOT NULL,
--     seconds INTEGER NOT NULL,
--     FOREIGN KEY (class_id) REFERENCES classes(id)
-- );

-- ALTER TABLE users
-- RENAME COLUMN user TO username;

-- CREATE TABLE times (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     class_id INTEGER NOT NULL,
--     seconds INTEGER NOT NULL, 
--     user_id INTEGER NOT NULL, 
--     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (user_id) REFERENCES users(id)
--     FOREIGN KEY (class_id) REFERENCES classes(id)
-- );