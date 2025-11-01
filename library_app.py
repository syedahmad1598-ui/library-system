from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# ---------------- Data ----------------
books = []
members = []
transactions = []

# ---------------- HTML Template ----------------
html = """
<!DOCTYPE html>
<html>
<head>
    <title>Library Management System</title>
    <style>
        body { font-family: Arial; background-color: #f2f2f2; padding: 20px; }
        h1, h2 { color: #333; }
        form { background: #fff; padding: 15px; border-radius: 10px; width: 400px; margin-bottom: 20px; }
        input, select { width: 100%; padding: 8px; margin: 5px 0; }
        button { padding: 8px 12px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; background: #fff; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>📚 Library Management System</h1>

    <h2>Add Book</h2>
    <form method="POST" action="/add_book">
        <input type="text" name="book_id" placeholder="Book ID" required>
        <input type="text" name="title" placeholder="Book Title" required>
        <input type="text" name="author" placeholder="Author" required>
        <button type="submit">Add Book</button>
    </form>

    <h2>Add Member</h2>
    <form method="POST" action="/add_member">
        <input type="text" name="member_id" placeholder="Member ID" required>
        <input type="text" name="name" placeholder="Member Name" required>
        <button type="submit">Add Member</button>
    </form>

    <h2>Issue Book</h2>
    <form method="POST" action="/issue_book">
        <select name="book_id" required>
            <option value="">Select Book</option>
            {% for book in books if book.available %}
            <option value="{{ book.book_id }}">{{ book.title }}</option>
            {% endfor %}
        </select>
        <select name="member_id" required>
            <option value="">Select Member</option>
            {% for member in members %}
            <option value="{{ member.member_id }}">{{ member.name }}</option>
            {% endfor %}
        </select>
        <button type="submit">Issue</button>
    </form>

    <h2>Return Book</h2>
    <form method="POST" action="/return_book">
        <select name="book_id" required>
            <option value="">Select Book to Return</option>
            {% for t in transactions if not t.returned %}
            <option value="{{ t.book_id }}">{{ t.book_title }}</option>
            {% endfor %}
        </select>
        <button type="submit">Return</button>
    </form>

    <h2>Books List</h2>
    <table>
        <tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th></tr>
        {% for book in books %}
        <tr>
            <td>{{ book.book_id }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.author }}</td>
            <td>{{ "Available" if book.available else "Issued" }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>Members List</h2>
    <table>
        <tr><th>ID</th><th>Name</th></tr>
        {% for member in members %}
        <tr><td>{{ member.member_id }}</td><td>{{ member.name }}</td></tr>
        {% endfor %}
    </table>

    <h2>Transactions</h2>
    <table>
        <tr><th>Book</th><th>Member</th><th>Status</th></tr>
        {% for t in transactions %}
        <tr>
            <td>{{ t.book_title }}</td>
            <td>{{ t.member_name }}</td>
            <td>{{ "Returned" if t.returned else "Issued" }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# ---------------- Data Classes ----------------
class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.available = True

class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

class Transaction:
    def __init__(self, book_id, book_title, member_id, member_name):
        self.book_id = book_id
        self.book_title = book_title
        self.member_id = member_id
        self.member_name = member_name
        self.returned = False

# ---------------- Routes ----------------
@app.route("/")
def home():
    return render_template_string(html, books=books, members=members, transactions=transactions)

@app.route("/add_book", methods=["POST"])
def add_book():
    new_book = Book(request.form["book_id"], request.form["title"], request.form["author"])
    books.append(new_book)
    return redirect("/")

@app.route("/add_member", methods=["POST"])
def add_member():
    new_member = Member(request.form["member_id"], request.form["name"])
    members.append(new_member)
    return redirect("/")

@app.route("/issue_book", methods=["POST"])
def issue_book():
    book_id = request.form["book_id"]
    member_id = request.form["member_id"]
    for book in books:
        if book.book_id == book_id and book.available:
            book.available = False
            for member in members:
                if member.member_id == member_id:
                    new_t = Transaction(book.book_id, book.title, member.member_id, member.name)
                    transactions.append(new_t)
                    break
            break
    return redirect("/")

@app.route("/return_book", methods=["POST"])
def return_book():
    book_id = request.form["book_id"]
    for t in transactions:
        if t.book_id == book_id and not t.returned:
            t.returned = True
            for b in books:
                if b.book_id == book_id:
                    b.available = True
                    break
            break
    return redirect("/")

# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True)
