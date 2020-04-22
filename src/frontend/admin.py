from flask import Flask, render_template, request, redirect, url_for, Markup, flash, Blueprint
from flaskext.mysql import MySQL
import sendgrid
import os
import string
import random
from sendgrid.helpers.mail import *
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask import send_from_directory




UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

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
@app.route('/viewbooks', methods=['GET', 'POST'])
def viewbooks():
    if request.method == "POST":
        searchfilter = request.form['searchfilter']
        if searchfilter == 'Title':
            cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book WHERE title = %s ",request.form['search'])

        elif searchfilter == 'Subject':
            cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book WHERE category = %s ",request.form['search'])

        elif searchfilter == 'ISBN':
            cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book WHERE isbn = %s ",request.form['search'])

        elif searchfilter == 'Author':
            cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book WHERE authorName = %s ",request.form['search'])

        elif searchfilter == 'Clear':
            cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book;")

        book = cursor.fetchall()
        return render_template('manage_books.html',searchfilter=searchfilter,book=book)
    else:
        cursor.execute("SELECT isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename FROM book;")
        book = cursor.fetchall()
        return render_template('manage_books.html',book=book)
    render_template('manage_books.html',book=book)

#route for main only for logged in users
@app.route('/viewspecificbook')
def viewspecificbook():
    isbn = request.args.get('isbn')
    print(isbn)
    cursor.execute("SELECT isbn, title, authorName FROM book where isbn=%s;", (isbn))
    book = cursor.fetchall()

    return render_template('edit_book.html',book=book)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

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

        file = request.files['coverPicture']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))



        #check for duplicate isbn
        cursor.execute("SELECT isbn FROM book;")
        fetchedisbn = cursor.fetchall()

        duplicateisbn = False

        for fetchedisbnS in fetchedisbn:
            if fetchedisbnS:
                fetchedisbnS=fetchedisbnS[0]
                if isbn == fetchedisbnS:
                    duplicateisbn = True

        if duplicateisbn == False:
            cursor.execute("INSERT INTO book(isbn,category,authorName,title,edition,publisher,publicationYear,quantityInStock,buyingPrice,sellingPrice,bookRating,filename) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (isbn,category,author,title,edition,publisher,publicationYear,quantity,buyingPrice,sellingPrice,rating,filename))
        else:
            message = Markup("<post>Duplicate ISBN. Please enter a unique ISBN.</post><br>")
            flash(message)
            return render_template('edit_book.html')

        con.commit()

        return redirect(url_for('viewbooks'))
    return render_template('edit_book.html')





if __name__ == '__main__':
    app.run(debug=True)
