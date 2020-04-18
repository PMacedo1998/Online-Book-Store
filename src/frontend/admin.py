from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import sendgrid
import os
import string
import random
from sendgrid.helpers.mail import *
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = "admin"
app.config['MYSQL_DATABASE_PASSWORD'] = "password"
app.config['MYSQL_DATABASE_DB'] = "bookstore"
app.config['MYSQL_DATABASE_HOST'] = "bookstore.cxp6si0l0mcz.us-east-2.rds.amazonaws.com"
mysql = MySQL(app)

con = mysql.connect()
cursor=con.cursor()

#route for main only for logged in users
@app.route('/')
def admin():
    return render_template('admin.html')

#route for main only for logged in users
@app.route('/viewbooks')
def viewbooks():
    cursor.execute("SELECT isbn FROM book;")
    isbn = cursor.fetchall()

    cursor.execute("SELECT title FROM book;")
    title = cursor.fetchall()

    cursor.execute("SELECT authorName FROM book;")
    authorName=cursor.fetchall()

    return render_template('manage_books.html',isbn=isbn,title=title,author=authorName)

#route for main only for logged in users
@app.route('/addbook')
def displaybookinfo():
    #from view books page
    return render_template('edit_book.html')

#route for main only for logged in users
@app.route('/addbook', methods = ['GET','POST'])
def addbook():
    if request.method == 'POST':

        #add book info
        isbn = request.form['isbn']
        category = request.form['category']
        author = request.form['author']
        title = request.form['title']
        edition = request.form['edition']
        publisher = request.form['publisher']
        publicationYear = request.form['publicationYear']
        quantity = request.form['quantity']
        buyingPrice = request.form['buyingPrice']
        sellingPrice = request.form['sellingPrice']
        rating = request.form['rating']
        coverPicture = request.form['coverPicture']

        cursor.execute("INSERT INTO book(isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,coverPicture) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (isbn,category,authorName,title,edition,publisher,publicationYear,quantity,buyingPrice,sellingPrice,rating,coverPicture))

        con.commit()

        return redirect(url_for('viewbooks'))
    return render_template('edit_book.html')

if __name__ == '__main__':
    app.run(debug=True)
