DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS working_hour;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL 
);

CREATE TABLE project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT UNIQUE NOT NULL,
    parent_id INTEGER NULL,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (role_id) REFERENCES role (id),
    FOREIGN KEY (parent_id) REFERENCES project (id)
);

CREATE TABLE working_hour (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    started TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    finished TIMESTAMP NULL,
    hours_total FLOAT NULL,
    label TEXT NULL,
    state BOOL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES project (id)
    FOREIGN Key (user_id) REFERENCES user (id)
);

CREATE TABLE role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT UNIQUE NOT NULL
);