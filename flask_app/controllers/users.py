from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.book import Book
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():
    if request.form['password'] != request.form['confirm_password']:
        flash("password and confirm password do not match")
        return redirect('/')
    data={"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if user_in_db:
        flash("email already exists!")
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print ("generated password hash:",pw_hash)

    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash,
    }
    user_id = User.save(data)
    if not user_id:
        flash("Registration failed. Please try again.")
        return redirect('/')
    
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {"email": request.form['email']}
    user_in_db = User.get_one_by_email(data)
    if not user_in_db:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/') 

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("please log in")
        return redirect('/login')
    books = Book.get_books_w_creator()
    user = User.get_one_by_id({"id": session['user_id']})
    return render_template('dashboard.html', books=books, user=user)

@app.route('/user/new')
def user_form():
    return render_template('dashboard.html')

@app.route('/user/<int:id>/edit')
def edit_form(id):
    data = {"id":id}
    user = User.get_one_by_id(data)
    user_books = Book.get_books_by_user(data)
    return render_template('account.html', user=user, user_books=user_books)

@app.route('/user/update', methods = ['POST'])
def update_user():
    user_data = {
        "id": request.form['id'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    if not User.validate_user_update(user_data):
        return redirect('/user/account')
    User.update(user_data)
    return redirect('/user/account')

@app.route('/user_list')
def user_list():
    users = User.get_users_w_books()
    return render_template('user_list.html', users=users)

#might want to un comment out below
# @app.route('/add_favorite/<int:book_id>')
# def add_favorite(book_id):
#     if 'user_id' not in session:
#         flash("Please login to favorite books")
#         return redirect('/')
    
#     data = {
#         "user_id": session['user_id'],
#         "book_id": book_id
#     }
#     Book.add_to_favorites(data)
#     return redirect('/dashboard')

# @app.route('/remove_favorite/<int:book_id>')
# def remove_favorite(book_id):
#     if 'user_id' not in session:
#         flash("Please login to unfavorite books")
#         return redirect('/')
    
#     data = {
#         "user_id": session['user_id'],
#         "book_id": book_id
#     }
#     Book.remove_from_favorites(data)
#     return redirect('/dashboard')















