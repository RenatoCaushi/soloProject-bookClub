from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Book:
    db_name = "book_club"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.users_id = data['users_id']
       

    @classmethod
    def new_book(cls, data):
        query = "INSERT INTO book (title, description, users_id) VALUES (%(title)s,%(description)s, %(users_id)s);"
        return  connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM book LEFT JOIN users on book.users_id = users.id LEFT JOIN likes on likes.book_id = book.id GROUP BY book.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        books = []
        if results:
            for row in results:
                books.append(row)
            return books
        return books


    @classmethod
    def get_book_by_title(cls, data):
        query = "SELECT * FROM book WHERE title = %(title)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        if len(result) < 1:
            return False
        return result[0]

    @classmethod
    def get_book_by_id(cls, data):
        query = "SELECT * FROM book LEFT JOIN users on book.users_id = users.id LEFT JOIN likes on likes.book_id = book.id WHERE book.id = %(book_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    @classmethod
    def get_book_by_likes(cls, data):
        query = "SELECT * FROM book WHERE id = %(book_id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    @classmethod
    def update(cls, data):
        query = "UPDATE book SET description = %(description)s WHERE book.id = %(book_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM book WHERE book.id = %(book_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
         
    
    @classmethod
    def deleteFans(cls, data):
        query = "DELETE FROM likes WHERE book_id = %(book_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
         
    
    @staticmethod
    def validate_book(data):
        is_valid = True
        if len(data['title'])<2:
                flash("*Title is required", 'title')
                is_valid = False
        if len(data['description']) < 5:
                flash("*Description must be at least 5 characters",  'desc')
                is_valid = False
        return is_valid    

    @classmethod
    def addLike(cls, data):
        query= 'INSERT INTO likes (book_id, user_id) VALUES ( %(book_id)s, %(user_id)s);'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeLike(cls, data):
        query= 'DELETE FROM likes WHERE book_id = %(book_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)