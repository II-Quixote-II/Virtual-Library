import streamlit as st
import sqlite3
import pandas as pd

# Database helpers 

def get_conn():
    return sqlite3.connect("database.db", check_same_thread=False)

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            id           INTEGER PRIMARY KEY,
            Title        TEXT NOT NULL,
            Author       TEXT NOT NULL,
            Genre        TEXT,
            Read_Status  TEXT DEFAULT 'UNREAD',
            Rating       TEXT,
            Date_Started TEXT,
            Date_Finished TEXT
        )
    """)
    conn.commit()
    conn.close()

def fetch_all() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM Books", conn)
    conn.close()
    return df

def fetch_by_id(book_id: int) -> pd.Series | None:
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM Books WHERE id = ?", conn, params=(book_id,))
    conn.close()
    return df.iloc[0] if not df.empty else None

def add_book(title, author, genre, rating, read_status, date_started, date_finished):
    conn = get_conn()
    conn.execute(
        """INSERT INTO Books (Title, Author, Genre, Rating, Read_Status, Date_Started, Date_Finished)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (title, author, genre or None, rating, read_status,
         str(date_started) if date_started else None,
         str(date_finished) if date_finished else None),
    )
    conn.commit()
    conn.close()

def update_book(book_id, title, author, genre, rating, read_status, date_started, date_finished):
    conn = get_conn()
    conn.execute(
        """UPDATE Books
           SET Title=?, Author=?, Genre=?, Rating=?, Read_Status=?,
               Date_Started=?, Date_Finished=?
           WHERE id=?""",
        (title, author, genre or None, rating, read_status,
         str(date_started) if date_started else None,
         str(date_finished) if date_finished else None,
         book_id),
    )
    conn.commit()
    conn.close()

def delete_book(book_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM Books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

# UI helpers

STATUS_OPTIONS = ["Unread", "Reading", "Read"]
RATING_OPTIONS = ["", "1 ✨", "2 ✨✨", "3 ✨✨✨", "4 ✨✨✨✨", "5 ✨✨✨✨✨"]

def book_form(key_prefix: str, defaults: dict | None = None):
    """Renders share form fields. Returns dict of values."""
    d = defaults or {}
    col1, col2 = st.columns(2)
    with col1:
        title  = st.text_input("Title *",  value=d.get("Title", ""),  key=f"{key_prefix}_title")
        author = st.text_input("Author *", value=d.get("Author", ""), key=f"{key_prefix}_author")
        genre  = st.text_input("Genre",    value=d.get("Genre") or "", key=f"{key_prefix}_genre")
        rating = st.selectbox("Rating", RATING_OPTIONS,
                              index=RATING_OPTIONS.index(d.get("Rating", "")) if d.get("Rating") in RATING_OPTIONS else 0,
                              key=f"{key_prefix}_rating")
    with col2:
        status = st.selectbox("Read Status", STATUS_OPTIONS,
                              index=STATUS_OPTIONS.index(d.get("Read_Status", "UNREAD")),
                              key=f"{key_prefix}_status")
        ds_val = pd.to_datetime(d.get("Date_Started"), errors="coerce")
        df_val = pd.to_datetime(d.get("Date_Finished"), errors="coerce")
        date_started  = st.date_input("Date Started",  value=ds_val if pd.notna(ds_val) else None,
                                      key=f"{key_prefix}_ds")
        date_finished = st.date_input("Date Finished", value=df_val if pd.notna(df_val) else None,
                                      key=f"{key_prefix}_df")

    return dict(title=title, author=author, genre=genre, rating=rating,
                read_status=status, date_started=date_started, date_finished=date_finished)

# Main Library App

def main():
    st.set_page_config(page_title="Book Tracker", page_icon="🦉", layout="wide")
    st.title("🦉 Book Tracker")

    init_db()

    tab_view, tab_add, tab_edit, tab_delete = st.tabs(
        ["Library", "+ Add Book", "Edit Book", "- Delete Book"]
    )

    # Tab 1 - View
    with tab_view:
        df = fetch_all()

        # Filter row
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            status_filter = st.selectbox("Status", ["All"] + STATUS_OPTIONS, key="filter_status")
        with col2:
            genre_filter = st.text_input("Genre contains", key="filter_genre")
        with col3:
            search = st.text_input("Search title / author", key="search")

        if status_filter != "All":
            df = df[df["Read_Status"] == status_filter]
        if genre_filter:
            df = df[df["Genre"].str.contains(genre_filter, case=False, na=False)]
        if search:
            mask = (
                df["Title"].str.contains(search, case=False, na=False)
                | df["Author"].str.contains(search, case=False, na=False)
            )
            df = df[mask]

        st.dataframe(df, use_container_width=True, hide_index=True)

        cols = st.columns(3)
        cols[0].metric("Total shown", len(df))
        cols[1].metric("Read",    len(df[df["Read_Status"] == "Read"]))
        cols[2].metric("Unread",  len(df[df["Read_Status"] == "Unread"]))

    # Tab 2 - Add
    with tab_add:
        st.subheader("Add a new book")
        with st.form("add_form"):
            vals = book_form("add")
            if st.form_submit_button(" Add Book", type="primary"):
                if vals["title"] and vals["author"]:
                    add_book(**vals)
                    st.success(f"✅ **{vals['title']}** added to your library!")
                    st.balloons()
                else:
                    st.error("Title and Author are required.")

    # Tab 3 - Edit
    with tab_edit:
        st.subheader("Edit an existing book")
        df_all = fetch_all()
        if df_all.empty:
            st.info("No books yet, Add some!")
        else:
            book_labels = {row["Title"]: row["id"] for _, row in df_all.iterrows()}
            selected_title = st.selectbox("Select book to edit", list(book_labels.keys()), key="edit_select")
            selected_id    = book_labels[selected_title]
            book           = fetch_by_id(selected_id)

            with st.form("edit_form"):
                vals = book_form("edit", defaults=book.to_dict())
                if st.form_submit_button(" Save Changes", type="primary"):
                    if vals["title"] and vals["author"]:
                        update_book(selected_id, **vals)
                        st.success(f"✅ **{vals['title']}** updated!")
                        st.rerun()
                    else:
                        st.error("Title and Author are required.")

    # fourth tab - Delete
    with tab_delete:
        st.subheader("Delete a book")
        df_all = fetch_all()
        if df_all.empty:
            st.info("Nothing to delete yet.")
        else:
            book_labels = {row["Title"]: row["id"] for _, row in df_all.iterrows()}
            selected_title = st.selectbox("Select book to delete", list(book_labels.keys()), key="del_select")
            selected_id    = book_labels[selected_title]

            st.warning("This will permanently delete **{selected_title}**.")
            confirm = st.checkbox("Yes", key="del_confirm")
            if st.button("Delete", type="primary", disabled=not confirm):
                delete_book(selected_id)
                st.success("**{selected_title}** deleted.")
                st.rerun()


if __name__ == "__main__":
    main()
