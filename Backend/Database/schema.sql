CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    middle_name_init TEXT,
    last_name TEXT NOT NULL,
    birthday DATE
);

CREATE TABLE e_address (
    id INTEGER,
    address TEXT NOT NULL,
    PRIMARY KEY (id, address),
    FOREIGN KEY (id) REFERENCES contacts(id)
)