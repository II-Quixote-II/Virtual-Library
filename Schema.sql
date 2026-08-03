CREATE TABLE IF NOT EXISTS Books (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    Title         TEXT NOT NULL,
    Author        TEXT NOT NULL,
    Genre         TEXT,
    Read_status   TEXT NOT NULL DEFAULT 'UNREAD'
                  CHECK (Read_status IN ('UNREAD', 'READING', 'READ', 'DNF')),
    Rating        INTEGER CHECK (Rating BETWEEN 1 AND 5),
    Date_Started  TEXT,
    Date_Finished TEXT
);
