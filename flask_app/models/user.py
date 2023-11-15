from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.password = data.get('password', None)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('bookclub_db').query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL('bookclub_db').query_db(query)
        users = []
        for user in result:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_one_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('bookclub_db').query_db(query, data)
        print("User data retrieved by email:", result)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('bookclub_db').query_db(query, data)
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email/password")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters",)
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords don't match")
        return is_valid
    
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s"
        return connectToMySQL('bookclub_db').query_db(query, data)
    
    @staticmethod
    def validate_user_update(user_data):
        is_valid = True
        if len(user_data['first_name']) < 2:
            flash("First name must be at least 2 characters")
            is_valid = False
        if len(user_data['last_name']) < 2:
            flash("Last name must be at least 2 characters")
            is_valid = False
        if not EMAIL_REGEX.match(user_data['email']):
            flash("Invalid email format")
            is_valid = False
        return is_valid

    @classmethod
    def get_users_w_books(cls):
        query = "SELECT * FROM users JOIN books ON users-id = books.user_id"
        results = connectToMySQL('bookclub_db').query_db(query)
        print(results)

        if results:
            new_result = []
            for row in results:
                user = cls(row)
                data = {
                    "id": row['books.id'],
                    "title": row['title'],
                    "description": row['description'],
                    "user_id": row['user_id'],
                    "created_at": row['books.created_at'],
                    "updated_at": row['books.updated_at'],
                }
                user.books.append(book.Book(data))
                new_result.append(user)
            return new_result

    @classmethod
    def get_all_users_who_favorited(cls, data):
        query = "SELECT * FROM favorites JOIN users ON favorites.users_id = users.id WHERE favorites.books_id = %(id)s"
        results = connectToMySQL('bookclub_db').query_db(query, data) #trying to pass in the favorited books by a user
        users = []
        if results:
            for row in results:
                user = cls(row)
                users.append(user)
            return users
        return users 
