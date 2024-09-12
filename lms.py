import streamlit as st

# ------------------- Backend (Data Structure-Based) -------------------

# Simulated databases using in-memory data structures
if 'books' not in st.session_state:
    st.session_state.books = {}  # {book_id: {"title": str, "author": str, "available": bool, "borrower": member_id or None}}
if 'members' not in st.session_state:
    st.session_state.members = {}  # {member_id: {"name": str, "borrowed_books": []}}

# Function to add a new book
def add_book(book_id, title, author):
    if book_id not in st.session_state.books:
        st.session_state.books[book_id] = {"title": title, "author": author, "available": True, "borrower": None}
        return f'Book "{title}" added successfully with ID "{book_id}".'
    return "Book already exists."

# Function to register a new member
def register_member(member_id, name):
    if member_id not in st.session_state.members:
        st.session_state.members[member_id] = {"name": name, "borrowed_books": []}
        return f'Member "{name}" registered successfully with ID "{member_id}".'
    return "Member already exists."

# Function to issue a book to a member
def issue_book(book_id, member_id):
    if book_id not in st.session_state.books:
        return "Book not found."
    if not st.session_state.books[book_id]["available"]:
        return "Book is already issued."
    if member_id not in st.session_state.members:
        return "Member not found."

    # Update book availability and record the borrower
    st.session_state.books[book_id]["available"] = False
    st.session_state.books[book_id]["borrower"] = member_id
    st.session_state.members[member_id]["borrowed_books"].append(book_id)
    return f'Book "{st.session_state.books[book_id]["title"]}" issued to member "{st.session_state.members[member_id]["name"]}".'

# Function to return a book
def return_book(book_id, member_id):
    if book_id not in st.session_state.books:
        return "Book not found."
    if st.session_state.books[book_id]["borrower"] != member_id:
        return "This member did not borrow this book."

    # Update book availability and remove it from the member's borrowed books
    st.session_state.books[book_id]["available"] = True
    st.session_state.books[book_id]["borrower"] = None
    st.session_state.members[member_id]["borrowed_books"].remove(book_id)
    return f'Book "{st.session_state.books[book_id]["title"]}" returned by member "{st.session_state.members[member_id]["name"]}".'

# Function to view all books
def view_books():
    available_books = {k: v for k, v in st.session_state.books.items() if v["available"]}
    issued_books = {k: v for k, v in st.session_state.books.items() if not v["available"]}
    return available_books, issued_books

# Function to view all members
def view_members():
    return st.session_state.members

# ------------------- Streamlit Frontend (UI) -------------------

# Streamlit UI
st.title("Library Management System (In-memory Data Structure)")

# Sidebar menu
menu = ["Add Book", "Register Member", "Issue Book", "Return Book", "View Books", "View Members"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Book Section
if choice == "Add Book":
    st.subheader("Add a New Book")
    book_id = st.text_input("Book ID", key="add_book_id")
    title = st.text_input("Book Title", key="add_title")
    author = st.text_input("Author", key="add_author")
    if st.button("Add Book"):
        if book_id and title and author:
            result = add_book(book_id, title, author)
            st.success(result)
        else:
            st.error("Please provide all details.")

# Register Member Section
elif choice == "Register Member":
    st.subheader("Register a New Member")
    member_id = st.text_input("Member ID", key="register_member_id")
    name = st.text_input("Member Name", key="register_name")
    if st.button("Register Member"):
        if member_id and name:
            result = register_member(member_id, name)
            st.success(result)
        else:
            st.error("Please provide all details.")

# Issue Book Section
elif choice == "Issue Book":
    st.subheader("Issue a Book")
    book_id = st.text_input("Book ID", key="issue_book_id")
    member_id = st.text_input("Member ID", key="issue_member_id")
    if st.button("Issue Book"):
        if book_id and member_id:
            result = issue_book(book_id, member_id)
            st.success(result)
        else:
            st.error("Please provide both Book ID and Member ID.")

# Return Book Section
elif choice == "Return Book":
    st.subheader("Return a Book")
    book_id = st.text_input("Book ID", key="return_book_id")
    member_id = st.text_input("Member ID", key="return_member_id")
    if st.button("Return Book"):
        if book_id and member_id:
            result = return_book(book_id, member_id)
            st.success(result)
        else:
            st.error("Please provide both Book ID and Member ID.")

# View Books Section
elif choice == "View Books":
    st.subheader("View Available and Issued Books")
    available_books, issued_books = view_books()

    st.write("### Available Books:")
    if available_books:
        for book_id, details in available_books.items():
            st.write(f"ID: {book_id}, Title: {details['title']}, Author: {details['author']}")
    else:
        st.write("No available books.")

    st.write("### Issued Books:")
    if issued_books:
        for book_id, details in issued_books.items():
            st.write(f"ID: {book_id}, Title: {details['title']}, Author: {details['author']}, Borrower: {details['borrower']}")
    else:
        st.write("No issued books.")

# View Members Section
elif choice == "View Members":
    st.subheader("View Registered Members")
    members = view_members()
    if members:
        for member_id, details in members.items():
            st.write(f"ID: {member_id}, Name: {details['name']}, Borrowed Books: {details['borrowed_books']}")
    else:
        st.write("No members registered yet.")
