CREATE TABLE Books (
    id            INTEGER PRIMARY KEY,
    Title         TEXT NOT NULL,
    Author        TEXT NOT NULL,
    Genre         TEXT,
    Read_status   TEXT DEFAULT 'UNREAD',
    Rating        TEXT NOT NULL,
    Date_Started  TEXT,
    Date_Finished TEXT
);
