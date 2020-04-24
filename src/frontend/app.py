from flask import Flask, render_template, request, redirect, url_for, Markup, flash, sessions, session, Blueprint
from flaskext.mysql import MySQL
import sendgrid
import os
import string
import random
from sendgrid.helpers.mail import *
from passlib.hash import sha256_crypt




app = Flask(__name__)



app.secret_key = 'secret'
app.config['MYSQL_DATABASE_USER'] = "admin"
app.config['MYSQL_DATABASE_PASSWORD'] = "password"
app.config['MYSQL_DATABASE_DB'] = "bookstore"
app.config['MYSQL_DATABASE_HOST'] = "bookstore.cxp6si0l0mcz.us-east-2.rds.amazonaws.com"
mysql = MySQL(app)

con = mysql.connect()
cursor=con.cursor()

#this app.route is specific to register page


@app.route('/bookdetails')
def bookdetails():
    return render_template('book_details.html')

@app.route('/checkout/<isbn>')
def checkout(isbn):
    return render_template('checkout.html',isbn=isbn)

@app.route('/checkoutmenu')
def checkout1():
    return render_template('checkout.html')




#route for main only for logged in users
@app.route('/main', methods = ['GET','POST'])
def main():
    if request.method == "POST":

        search=None
        addbooktocart=None
        isbn=None
        #searchfilter
        if request.form['submit_button'] == 'search':
            search=True
        else:
            isbn=request.form['submit_button']
            addbooktocart=True
            print("isbn is " + str(isbn))
        print("addbooktocart is " + str(addbooktocart))
        print("search is " + str(search))


        searchfilter = request.form['searchfilter']
        #viewdetails

        if search == True:
            if searchfilter == 'Title':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE title = %s ",request.form['search'])

            elif searchfilter == 'Subject':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE category = %s ",request.form['search'])

            elif searchfilter == 'ISBN':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE isbn = %s ",request.form['search'])

            elif searchfilter == 'Author':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE authorName = %s ",request.form['search'])

            elif searchfilter == '':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book;")
            book = cursor.fetchall()
            return render_template('logged_in_homepage.html',searchfilter=searchfilter,book=book)
        elif addbooktocart == True:

            return redirect(url_for('checkout',isbn=isbn))

    else:
        cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book;")
        book = cursor.fetchall()
    return render_template('logged_in_homepage.html',book=book)

#route for forgotten password
@app.route('/forgotPassword', methods = ['GET', 'POST'])
def forgotPassword():
    inputEmail=''
    if request.method == 'POST':

        inputEmail = request.form['email']
        cursor.execute('SELECT * FROM profile')
        users = cursor.fetchall()
        #generate random code
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        for x in users:
            email = x[4]
            if inputEmail == email: #account found
                #generate verification email
                message = 'You are receiving this email because you requested a password reset. Please enter the following code on the webpage to verify this request: ' + code
                mail = Mail(from_email = 'tylerrosen97@gmail.com',
                            to_emails = request.form['email'],
                            subject = 'Bookstore password reset',
                            plain_text_content = message
                            )

                #send verification email
                sg = sendgrid.SendGridAPIClient(api_key='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')
                response = sg.client.mail.send.post(request_body=mail.get())

                #store code
                cursor.execute ("""
                                UPDATE profile
                                SET verificationCode=%s
                                WHERE email=%s
                                """, (code, inputEmail))
                con.commit()
                return redirect(url_for('resetPassword'))
    return render_template("forgotPassword.html")



#route to reset forgotten password
@app.route('/resetPassword',  methods = ['GET', 'POST'])
def resetPassword():
    inputCode=''
    inputPass=''
    if request.method == 'POST':

        inputCode = request.form['code']
        inputPass = sha256_crypt.encrypt(request.form['password'])
        cursor.execute('SELECT * FROM profile')
        users = cursor.fetchall()
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        for x in users:

            code=x[7]
            if inputCode == code: #account found; need to make more secure
                #store new password
                cursor.execute ("""
                                UPDATE profile
                                SET pswd=%s
                                WHERE verificationCode=%s
                                """, (inputPass, code))
                con.commit()
                return render_template("passwordUpdated.html")
    return render_template("resetPassword.html")

#goes to this after submitting registration info
@app.route('/account_verification', methods = ['GET','POST'])
def verify():
    sessionID = session['id']
    inputCode=''
    if request.method == 'POST':
        cursor.execute("SELECT verificationCode FROM profile WHERE id=%s;", (sessionID))
        dbCode = cursor.fetchone()
        dbCode = dbCode[0]
        inputCode = request.form['code']
        verified = False
        accountId = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if inputCode == dbCode:
            verified = True

        if verified:
            message = Markup("<post>Account verification successful!</post><br>")
            flash(message)
            
        else:
            message = Markup("<post>Incorrect verification code</post><br>")
            flash(message)

    return render_template("account_verification.html")

#register function
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':

        #get personal info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password =sha256_crypt.encrypt(request.form['password'])
        phoneNumber = request.form['phoneNumber']

        #ensure account with this email does not already exist
        existingEmail = ''
        cursor.execute('SELECT * FROM profile')
        users = cursor.fetchall()
        previouslyRegistered = False

        for x in users:
            existingEmail = x[4]
            if existingEmail == email: #account with email already exists
                message = Markup("<post>An account with this email address already exists</post><br>")
                flash(message)
                return render_template("registration.html")

        #generate random code
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        #generate verification email
        mail = Mail(from_email = 'tylerrosen97@gmail.com',
                    to_emails = request.form['email'],
                    subject = 'Bookstore verification code',
                    plain_text_content = 'Your unique verification code is: ' + code
                    )

        #send verification email
        sg = sendgrid.SendGridAPIClient(api_key='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')
        response = sg.client.mail.send.post(request_body=mail.get())

        #get payment info
        name = request.form['name']
        cardType = request.form['cardType']
        cardNumber = sha256_crypt.encrypt(request.form['cardNumber'])
        expirationDate = request.form['expirationDate']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zip = request.form['zip']
        city = request.form['city']
        state = request.form['state']

        #store into dB
        cursor.execute("INSERT INTO profile(firstName, lastName, phoneNum, email, pswd, address1, address2, zipcode, city, state, verificationCode) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (firstName, lastName, phoneNumber, email, password, address1, address2, zip, city, state, code))
        cursor.execute("INSERT INTO paymentMethod(type, cardNumber, expirationDate, name) VALUES (%s,%s,%s,%s)", (cardType, cardNumber, expirationDate, name))

        con.commit()

        return render_template('registration_confirmation.html')
    return render_template('registration.html')
#logout
@app.route('/login/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    #return url_for('login')
    return render_template("login.html")

#login function
@app.route('/login/', methods = ['GET','POST'])
def login():
    inputEmail=''
    inputPass=''
    counter = 0
    if request.method == 'POST':

        inputEmail = request.form['email']
        inputPass = request.form['password']
        counter += 1

    cursor.execute('SELECT * FROM profile')
    users = cursor.fetchall()
    isUser = False


    for x in users:
        email = x[4]
        passWord = x[5]
        if inputEmail == email and sha256_crypt.verify(inputPass, passWord):
            isUser = True
            session['loggedin'] = True
            session['id'] = x[0]
    if isUser == False and counter != 0:
        message = Markup("<post>Incorrect email and/or password. Please try again.</post><br>")
        flash(message)
        return render_template("login.html")
    elif isUser == False:
        return render_template("login.html")
    print(session['id'])
    return redirect(url_for('main'))
 #   if request.method == 'GET':
        #get personal info
   #     return render_template("login.html",error=False)

 #   if request.form['email']!="email@gmail.com" or request.form['password']!= "password":
   #     return render_template('login.html',error = True)


    return render_template("login.html")

#change password
@app.route('/changePassword', methods=['GET', 'POST'])
def changePassword():
    sessionID = session['id']
    oldPass=''
    newPass=''
    dbPass=''

    if request.method == 'POST':
        cursor.execute("SELECT pswd FROM profile WHERE id=%s;",(sessionID))
        dbPass=cursor.fetchone()
        dbPass=dbPass[0]
        oldPass = request.form['oldPass']
        newPass = sha256_crypt.encrypt(request.form['newPass'])
        if  sha256_crypt.verify(oldPass, dbPass):
            cursor.execute("UPDATE profile SET pswd='{}' WHERE id=%s;".format(newPass), (sessionID))
            con.commit()
            return render_template("passwordUpdated.html")
        else:
            message = Markup("<post>Current password is incorrect</post><br>")
            flash(message)
    return render_template("edit_password.html")

#display profile information
@app.route('/editprofile')
def displayinfo():
    sessionID = session['id']
    cursor.execute("SELECT firstName FROM profile WHERE id=%s;",(sessionID))
    firstName = cursor.fetchone()
    if firstName:
        firstName=firstName[0]

    cursor.execute("SELECT lastName FROM profile WHERE id=%s;",(sessionID))
    lastName=cursor.fetchone()
    if lastName:
        lastName=lastName[0]

    cursor.execute("SELECT email FROM profile WHERE id=%s;", (sessionID))
    email=cursor.fetchone()
    if email:
        email=email[0]

    cursor.execute("SELECT phoneNum FROM profile WHERE id=%s;", (sessionID))
    phoneNumber=cursor.fetchone()
    if phoneNumber:
        phoneNumber=phoneNumber[0]

    cursor.execute("SELECT address1 FROM profile WHERE id=%s;", (sessionID))
    address1=cursor.fetchone()
    if address1:
        address1=address1[0]

    cursor.execute("SELECT address2 FROM profile WHERE id=%s;", (sessionID))
    address2=cursor.fetchone()
    if address2:
        address2=address2[0]

    cursor.execute("SELECT zipcode FROM profile WHERE id=%s;", (sessionID))
    zipcode=cursor.fetchone()
    if zipcode:
        zipcode=zipcode[0]

    cursor.execute("SELECT city FROM profile WHERE id=%s;", (sessionID))
    city=cursor.fetchone()
    if city:
        city=city[0]

    cursor.execute("SELECT state FROM profile WHERE id=%s;", (sessionID))
    state=cursor.fetchone()
    if state:
        state=state[0]

    cursor.execute("SELECT name FROM paymentMethod WHERE paymentMethodID=%s;", (sessionID))
    cardName=cursor.fetchone()
    if cardName:
        cardName=cardName[0]

    cursor.execute("SELECT type FROM paymentMethod WHERE paymentMethodID=%s;", (sessionID))
    cardType=cursor.fetchone()
    if cardType:
        cardType=cardType[0]

    cursor.execute("SELECT expirationDate FROM paymentMethod WHERE paymentMethodID=%s;", (sessionID))
    expirationDate=cursor.fetchone()
    if expirationDate:
        expirationDate=expirationDate[0]


    return render_template('edit_profile.html', fName=firstName,lName=lastName,email=email,phoneNum=phoneNumber,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,cardName=cardName,cardType=cardType,expirationDate=expirationDate)


#update profile information
@app.route('/editprofile', methods = ['GET','POST'])
def updateinfo():
    sessionID = session['id']
    if request.method == 'POST':

        #edit personal info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        cardName = request.form['cardName']
        cardType = request.form['cardType']
        cardNumber = request.form['cardNumber']
        expirationDate = request.form['expirationDate']

        #update into dB
        if(firstName!=''):
            cursor.execute("UPDATE profile SET firstName='{}' WHERE id=%s;".format(firstName), (sessionID))
        if(lastName!=''):
            cursor.execute("UPDATE profile SET lastName='{}' WHERE id=%s;".format(lastName), (sessionID)) 
        if(phoneNumber!=''):
            cursor.execute("UPDATE profile SET phoneNum='{}' WHERE id=%s;".format(phoneNumber), (sessionID))

        if(address1!=''):
            cursor.execute("UPDATE profile SET address1='{}' WHERE id=%s;".format(address1), (sessionID))

        if(address2!=''):
            cursor.execute("UPDATE profile SET address2='{}' WHERE id=%s;".format(address2), (sessionID))

        if(zipcode!=''):
            cursor.execute("UPDATE profile SET zipcode='{}' WHERE id=%s;".format(zipcode), (sessionID))

        if(city!=''):
            cursor.execute("UPDATE profile SET city='{}' WHERE id=%s;".format(city), (sessionID))

        if(state!=''):
            cursor.execute("UPDATE profile SET state='{}' WHERE id=%s;".format(state), (sessionID))

        if(cardName!=''):
            cursor.execute("UPDATE paymentMethod SET name='{}' WHERE paymentMethodID=%s;".format(cardName), (sessionID))

        if(cardType!=''):
            cursor.execute("UPDATE paymentMethod SET type='{}' WHERE paymentMethodID=%s;".format(cardType), (sessionID))

        if(cardNumber!=''):
            cursor.execute("UPDATE paymentMethod SET cardNumber='{}' WHERE paymentMethodID=%s;".format(cardNumber), (sessionID))

        if(expirationDate!=''):
            cursor.execute("UPDATE paymentMethod SET expirationDate='{}' WHERE paymentMethodID=%s;".format(expirationDate), (sessionID))



        con.commit()
        message = Markup("<post>Success! Your profile information was updated.</post><br>")
        flash(message)

        return redirect(url_for('displayinfo'))

    return render_template('edit_profile.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        search=None
        addbooktocart=None
        isbn=None
        #searchfilter
        if request.form['submit_button'] == 'search':
            search=True
        else:
            isbn=request.form['submit_button']
            addbooktocart=True
            print("isbn is " + str(isbn))
        #try:
        #    search=request.form['search']
        #except:
        #    addtocart=request.form['addtocart']
        #return render_template('book_details.html')



        print("addbooktocart is " + str(addbooktocart))
        print("search is " + str(search))


        searchfilter = request.form['searchfilter']
        #viewdetails

        if search == True:
            if searchfilter == 'Title':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE title = %s ",request.form['search'])

            elif searchfilter == 'Subject':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE category = %s ",request.form['search'])

            elif searchfilter == 'ISBN':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE isbn = %s ",request.form['search'])

            elif searchfilter == 'Author':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book WHERE authorName = %s ",request.form['search'])

            elif searchfilter == '':
                cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book;")
            book = cursor.fetchall()
            return render_template('homepage.html',searchfilter=searchfilter,book=book)
        elif addbooktocart == True:
            message = Markup("<post>You must be logged in to add book item to cart.</post><br>")
            flash(message)
            return redirect(url_for('login'))

    else:
        cursor.execute("SELECT title,authorName,sellingPrice,filename,isbn FROM book;")
        book = cursor.fetchall()
        return render_template('homepage.html',book=book)
    render_template('homepage.html',book=book)




if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)

