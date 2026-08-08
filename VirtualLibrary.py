import sqlite3
from pathlib import Path

DB_PATH = "Books.db"

VALID_STATUSES = ("UNREAD", "READING", "READ", "DNF")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn


def add_book(title: str, author: str, genre: str | None = None,
             read_status: str = "UNREAD") -> int:
    """Insert a new book and return its new id."""
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO Books (Title, Author, Genre, Read_status) "
            "VALUES (?, ?, ?, ?)",
            (title, author, genre, read_status),
        )
        return cur.lastrowid


def get_book(book_id: int) -> sqlite3.Row | None:
    with _connect() as conn:
        cur = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,))
        return cur.fetchone()


def find_books_by_title(title: str) -> list[sqlite3.Row]:
    """Case-insensitive partial match, e.g. find_books_by_title('quixote')."""
    with _connect() as conn:
        cur = conn.execute(
            "SELECT * FROM Books WHERE Title LIKE ? ORDER BY Title",
            (f"%{title}%",),
        )
        return cur.fetchall()


def list_all_books(order_by: str = "Title") -> list[sqlite3.Row]:
    allowed_columns = {"id", "Title", "Author", "Genre", "Read_status", "Rating"}
    if order_by not in allowed_columns:
        raise ValueError(f"Cannot sort by {order_by!r}")
    with _connect() as conn:
        cur = conn.execute(f"SELECT * FROM Books ORDER BY {order_by}")
        return cur.fetchall()


def update_read_status(book_id: int, status: str) -> None:
    status = status.upper()
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {VALID_STATUSES}")
    with _connect() as conn:
        conn.execute(
            "UPDATE Books SET Read_status = ? WHERE id = ?",
            (status, book_id),
        )


def update_genre(book_id: int, genre: str) -> None:
    with _connect() as conn:
        conn.execute("UPDATE Books SET Genre = ? WHERE id = ?", (genre, book_id))


def update_rating(book_id: int, rating: int) -> None:
    if not 1 <= rating <= 5:
        raise ValueError("rating must be between 1 and 5")
    with _connect() as conn:
        conn.execute("UPDATE Books SET Rating = ? WHERE id = ?", (rating, book_id))


def update_dates(book_id: int, date_started: str | None = None,
                  date_finished: str | None = None) -> None:

    with _connect() as conn:
        if date_started is not None:
            conn.execute(
                "UPDATE Books SET Date_Started = ? WHERE id = ?",
                (date_started, book_id),
            )
        if date_finished is not None:
            conn.execute(
                "UPDATE Books SET Date_Finished = ? WHERE id = ?",
                (date_finished, book_id),
            )


def delete_book(book_id: int) -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM Books WHERE id = ?", (book_id,))
