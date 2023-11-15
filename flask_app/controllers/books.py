from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.book import Book
from flask_app.models.user import User
from flask_app import app

# serves the book_form.html template
@app.route('/books/new') 
def book_form():
    return render_template('book_form.html')

# intended to create a new book using the Book.save method
@app.route('/books', methods=['POST'])
def create_book():
    data={
        "title":request.form['title'],
        "description":request.form['description'],
        "user_id": session['user_id']
    }
    Book.save(data)
    return redirect('/dashboard')

# This route fetches a single book by its ID and then fetches the corresponding user instance.
# @app.route('/books/<int:id>')
# def one_book(id):
#     data = {
#         "id":id
#         }
#     one_book = Book.get_book_by_id(data)
#     if one_book is None:
#         return "Error: Book not found", 404
#     user_instance = User.get_one_by_id({"id": one_book.user_id})
#     # This assumes you have a user_id property on the book instance
#     if hasattr(one_book, 'title'):
#         return render_template('show.html', one_book=one_book, user=user_instance)
#     else:
#         return "Error: The book does not have a title attribute.", 400
#     users_who_favorited = User.get_all_users_who_favorited()

@app.route('/books/<int:id>')
def one_book(id):
    if 'user_id' not in session:
        flash("Please log in to view this page")
        return redirect('/login')  # make sure this redirects to your login page

    user_data = {
        "id": session['user_id']
    }
    user = User.get_one_by_id(user_data)
    book_data = {
        "id": id
    }
    one_book = Book.get_book_by_id(book_data)
    users_who_favorited = User.get_all_users_who_favorited(book_data)
    return render_template('show.html', one_book=one_book, user=user, users_who_favorited=users_who_favorited)


# This route deletes a book by its ID and redirects to the /dashboard
@app.route('/books/<int:id>/delete')
def delete_book(id):
    book = Book.get_book_by_id({"id": id})
    if 'user_id' not in session or session['user_id'] != book.user_id:
        flash("You do not have permission to delete this book.")
        return redirect('/dashboard')
    
    Book.delete_book({"id": id})
    flash("Book deleted successfully")
    return redirect('/dashboard')

# It checks if a user is logged in and displays the user account details along with the books related to that user.
@app.route('/user/account')
def user_account():
    if 'user_id' not in session:
        flash("Please log in")
        return redirect('/')
    data = {"id": session['user_id']}
    user = User.get_one_by_id(data)
    user_books = Book.get_books_by_user(data)
    return render_template('account.html', user=user, user_books=user_books)

# to get one book and go to the edit page with form
@app.route('/books/<int:id>/edit')
def book_edit_form(id):
    book = Book.get_book_by_id({"id": id})
    if 'user_id' not in session or session['user_id'] != book.user_id:
        flash("You do not have permission to edit this book.")
        return redirect('/dashboard')
    
    return render_template('book_form.html', book=book)

@app.route('/books/<int:id>/update', methods=['POST', 'GET'])
def update_book(id):
    book = Book.get_book_by_id({"id": id})
    if 'user_id' not in session or session['user_id'] != book.user_id:
        flash("You do not have permission to update this book.")
        return redirect('/dashboard')

    data = {
        "id": id,
        "title": request.form['title'],
        "description": request.form['description'],
    }
    Book.update_book(data)
    flash("Book updated successfully")
    return redirect('/dashboard')

@app.route("/favorite/<int:id>")
def favorite_book(id):
    data = {
        "users_id": session['user_id'],
        "books_id": id
    }

    Book.add_favorite(data)
    return redirect('/dashboard')



# @app.route("/favorite/<int:book_id>")
# def favorite_book(book_id):
#     if 'user_id' not in session:
#         return redirect('/login')
#     data = {
#         "users_id": session['user_id'],
#         "books_id": book_id
#     }
#     if not Book.is_favorite(book_id, session['user_id']):
#         Book.add_favorite(data)
#     return redirect('/dashboard')

# @app.route("/unfavorite/<int:book_id>")
# def unfavorite_book(book_id):
#     if 'user_id' not in session:
#         return redirect('/login')
#     data = {
#         "users_id": session['user_id'],
#         "books_id": book_id
#     }
#     if Book.is_favorite(book_id, session['user_id']):
#         Book.remove_favorite(data)
#     return redirect('/dashboard')



# # This route adds a book to the user's favorites
# # for favorites button to work
# @app.route("/favorite/<int:id>")
# def favorite_book(id): 
#     data = {
#         "users_id": session['user_id'],
#         "books_id": id
#     }

#     Book.add_favorite(data)
#     return redirect('/dashboard') #or whatever page i want this to go to

