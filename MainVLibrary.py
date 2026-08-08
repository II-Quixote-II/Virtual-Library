# CLI Frontend 

# Option 1: "Add Book" is WIP - SQLite3.IntegrityError

import VirtualLibrary as library

MENU = """
Virtual Library
1) Add a book
2) List all books
3) Search by title
4) Update read status
5) Update rating
6) Delete a book
7) Quit
"""


def print_books(books) -> None:
    if not books:
        print("(no books found)")
        return
    for b in books:
        rating = b["Rating"] if b["Rating"] is not None else "-"
        genre = b["Genre"] if b["Genre"] else "-"
        print(f'  [{b["id"]}] {b["Title"]} by {b["Author"]}  '
              f'({b["Read_status"]}, genre: {genre}, rating: {rating})')


def main() -> None:
    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre (optional): ").strip() or None
            book_id = library.add_book(title, author, genre)
            print(f"Added '{title}' with id {book_id}")

        elif choice == "2":
            print_books(library.list_all_books())

        elif choice == "3":
            query = input("Search title for: ").strip()
            print_books(library.find_books_by_title(query))

        elif choice == "4":
            book_id = int(input("Book id: ").strip())
            status = input(f"New status {library.VALID_STATUSES}: ").strip()
            try:
                library.update_read_status(book_id, status)
                print("Updated.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            book_id = int(input("Book id: ").strip())
            try:
                rating = int(input("Rating (1-5): ").strip())
                library.update_rating(book_id, rating)
                print("Updated.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            book_id = int(input("Book id to delete: ").strip())
            confirm = input(f"Delete book {book_id}? (y/n): ").strip().lower()
            if confirm == "y":
                library.delete_book(book_id)
                print("Deleted.")

        elif choice == "7":
            print("Adios")
            break

        else:
            print("Not a valid option, try again.")


if __name__ == "__main__":
    main()
