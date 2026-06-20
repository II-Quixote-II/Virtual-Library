import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "VirtualLibrary.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

st.set_page_config(page_title="My Library", layout="wide")
st.title("My Library")

conn = get_connection()

# View Books

st.subheader("All Books")
df = pd.read_sql("SELECT * FROM Books", conn
st.dataframe(df, use_container_width=True)

st.divider()

# Add Book

st.subheader("Add a Book")
col1, col2 = st.columns(2)

with col1:
    title = st.text_input("Title")
    autgor = st.text_input("Author")
    genre = st.text_input("Genre")

with col2:
    rating = st.selectbox("Rating", options = list_range(1,10))
    read_status = st.selectbox("Read Status", options=["Not Started", "In Progress", "Completed"])

if st.button("Add Book", type="primary"):
    if title and author:
        curr = conn.cursor()
        curr.execute(
            "INSERT INTO Books (title, author, genre, rating, read_status) VALUES (?, ?, ?, ?, ?)", 
            (title, author, genre, rating, read_status)
        )
        conn.commit()
        st.success("Book added successfully!")
        st.rerun()
        else:
            st.error("Missing field(s)")

st.divider()

# Update Book

st.subheader("Update a Book")
if not df.empty
    book_id = st.selectbox("Select Book ID", options=df["id"], format_func=lambda x: df[df["id"]==x]["title"].values[0])
    if not df.empty:
    book_id = st.selectbox("Select book to update", df["id"], format_func=lambda x: df[df["id"]==x]["Title"].values[0])
    current = df[df["id"] == book_id].iloc[0]

    new_genre = st.text_input("New Genre", value=current["Genre"] or "")
    new_rating = st.selectbox("New Rating", list_range(1,10)
                                index= list_range(1,10).index(current["Rating"]) if current["Rating"] in list_range(1,10) else 0)

    if st.button("Save Changes"):
        cur = conn.cursor()
        cur.execute(
            "UPDATE Books SET Genre = ?, Rating = ? WHERE id = ?",
            (new_genre, new_rating, int(book_id))
        )          
        conn.commit()
        st.success("Book updated successfully!")
        st.rerun()

# Delete Book

st.subheader("Delete a Book")
if not df.empty:
    delete_id = st.selectbox("Select book to delete", df["id"], format_func=lambda x: df[df["id"]==x]["Title"].values[0], key="delete")
    if st.button("Delete", type="secondary"):
        cur = conn.cursor()
        cur.execute("DELETE FROM Books WHERE id = ?", (int(delete_id),))
        conn.commit()
        st.warning("Deleted")
        st.rerun()
