from flask_app import app
from flask_app.models.user import User
from flask_app.models.book import Book
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

@app.route('/books')
def booksPage():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    books = Book.get_all_books()
    userLikedPosts = User.get_logged_user_liked_posts(data)
    return render_template('newBook.html', user= user, books= books, userLikedPosts= userLikedPosts)


@app.route('/book/<int:id>')
def singleBook(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    user = User.get_user_by_id(data)
    book = Book.get_book_by_id(data)
    return render_template('singleBook.html', user= user, book= book)

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Book.addLike(data)
    return redirect(request.referrer)

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Book.removeLike(data)
    return redirect(request.referrer)

@app.route('/createBook', methods = ['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Book.validate_book(request.form):
        return redirect(request.referrer)
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'users_id': session['user_id'],
    }

    Book.new_book(data)
    return redirect(request.referrer)

    
@app.route('/update/description/<int:id>', methods = ['POST'])
def updateBook(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    book = Book.get_book_by_id(data)

    # ose book.users_id ose book['users_id']
    if (session['user_id'] != book['users_id']):
        return redirect(request.referrer)

    data2 = {
        'description': request.form['description'],
        'book_id': id
    }
    if len(request.form['description'])<5:
        flash("Description is required", "DescriptionUpdate")
        return redirect(request.referrer)
    Book.update(data2)
    return redirect(request.referrer)

@app.route('/delete/<int:id>')
def deleteBook(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id'],
        'book_id': id
    }
    book = Book.get_book_by_id(data)

    # ose book.users_id ose book['users_id']
    if (session['user_id'] != book['users_id']):
        return redirect(request.referrer)

    data2 = {
        'book_id': id
    }
    Book.deleteFans(data2)
    Book.delete(data2)
    return redirect('/')