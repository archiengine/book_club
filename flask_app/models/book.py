from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.favorited_by = [] #add in list when i have it 

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, description, user_id, created_at, updated_at) VALUES (%(title)s, %(description)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('bookclub_db').query_db(query,data)
    
    @classmethod
    def get_book_by_id(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL('bookclub_db').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_books_w_creator(cls):
        query="SELECT * FROM books JOIN users ON books.user_id = users.id"
        results = connectToMySQL('bookclub_db').query_db(query)
        all_books = []
        if results:
            for row in results:
                book = cls({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['user_id']
                })
                user_id = row['user.id'] if 'user.id' in row else None
                user_created_at = row['users.created_at'] if 'users.created_at' in row else None
                user_updated_at = row['users.updated_at'] if 'users.updated_at' in row else None
                data = {
                    'id':user_id,
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'created_at':user_created_at,
                    'updated_at':user_updated_at
                }
                book.creator = user.User(data)
                all_books.append(book)
        return all_books
    
    @classmethod
    def delete_book(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s"
        return connectToMySQL('bookclub_db').query_db(query, data)
    
    @classmethod
    def update_book(cls, data):
        query = "UPDATE books SET title=%(title)s, description=%(description)s WHERE id = %(id)s;"
        return connectToMySQL('bookclub_db').query_db(query, data)

    
    @classmethod
    def get_books_by_user(cls, data):
        query = "SELECT * FROM books WHERE user_id = %(id)s;"
        results = connectToMySQL('bookclub_db').query_db(query, data)
        return cls(results[0])

    @classmethod
    def one_book(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL('bookclub_db').query_db(query,data)
        if len(result) <1:
            return None
        return cls(result[0])
    
    # establishing the relationship to the favorites table
    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (users_id, books_id) VALUES (%(users_id)s, %(books_id)s)"
        return connectToMySQL('bookclub_db').query_db(query, data)
    

    # @classmethod
    # def is_favorite(cls, data):
    #     if 'id' not in data:
    #         raise ValueError("Missing id in data for retrieving favorites")
        
    #     query = "SELECT * FROM users JOIN favorites ON users.id = favorites.users_id JOIN books ON favorites.books_id = books.id WHERE users.id = %(id)s"
    #     results = connectToMySQL('bookclub_db').query_db(query, data)

    #     if not results:
    #         return[]
        
    #     processed_results = []
    #     for row in results:
    #         book_data = {
    #             'id': row['books.id'],
    #             'title': row['title'],
    #             'description': row['description'],
    #             'created_at': row['created_at'],
    #             'updated_at': row['updated_at'],
    #             'user_id': row['books.user_id']
    #         }
    #         book = cls(book_data)
            
    #         creator_data = {
    #             'id': row['users.id'],
    #             'first_name': row['first_name'],
    #             'last_name': row['last_name'],
    #             'email': row['email'],
    #             'created_at': row['created_at'],
    #             'updated_at': row['updated_at'],
    #         }
    #         creator = User(creator_data)
    #         book.creator = creator
    #         processed_results.append(book)
    #     return processed_results


