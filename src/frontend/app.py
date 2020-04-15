from flask import Flask, render_template, request, redirect, url_for
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

#this app.route is specific to register page

#route for homepage or INDEX
@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('homepage.html')

#route for main only for logged in users
@app.route('/main', methods = ['GET','POST'])
def main():
    return render_template('main.html')

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
    inputEmail=''
    inputCode=''
    if request.method == 'POST':

        inputEmail = request.form['email']
        inputCode = request.form['code']
        cursor.execute('SELECT * FROM profile')
        users = cursor.fetchall()
        verified = False

        for x in users:
            email = x[4]
            code = x[7]
            if inputEmail == email and inputCode == code:
                    verified = True
        if verified:
            return render_template("registration_confirmation.html")

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
                return render_template('exists.html')

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

        return redirect(url_for('verify'))
    return render_template('registration.html')

#login function
@app.route('/login/', methods = ['GET','POST'])
def login():
    inputEmail=''
    inputPass=''
    if request.method == 'POST':

        inputEmail = request.form['email']
        inputPass = request.form['password']

    cursor.execute('SELECT * FROM profile')
    users = cursor.fetchall()
    isUser = False


    for x in users:
        email = x[4]
        passWord = x[5]
        if inputEmail == email and sha256_crypt.verify(inputPass, passWord):
            isUser = True

    if isUser == False:
        return render_template("login.html")
    return render_template("logged_in_homepage.html")
 #   if request.method == 'GET':
        #get personal info
   #     return render_template("login.html",error=False)

 #   if request.form['email']!="email@gmail.com" or request.form['password']!= "password":
   #     return render_template('login.html',error = True)

    return render_template("login.html")

#display profile information
@app.route('/editprofile')
def displayinfo():

    cursor.execute("SELECT firstName FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    firstName = cursor.fetchone()
    if firstName:
        firstName=firstName[0]

    cursor.execute("SELECT lastName FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    lastName=cursor.fetchone()
    if lastName:
        lastName=lastName[0]

    cursor.execute("SELECT email FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    email=cursor.fetchone()
    if email:
        email=email[0]

    cursor.execute("SELECT phoneNum FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    phoneNumber=cursor.fetchone()
    if phoneNumber:
        phoneNumber=phoneNumber[0]

    cursor.execute("SELECT address1 FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    address1=cursor.fetchone()
    if address1:
        address1=address1[0]

    cursor.execute("SELECT address2 FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    address2=cursor.fetchone()
    if address2:
        address2=address2[0]

    cursor.execute("SELECT zipcode FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    zipcode=cursor.fetchone()
    if zipcode:
        zipcode=zipcode[0]

    cursor.execute("SELECT city FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    city=cursor.fetchone()
    if city:
        city=city[0]

    cursor.execute("SELECT state FROM profile WHERE id=(SELECT MAX(id) FROM profile);")
    state=cursor.fetchone()
    if state:
        state=state[0]

    cursor.execute("SELECT name FROM paymentMethod WHERE paymentMethodID=(SELECT MAX(paymentMethodID) FROM paymentMethod);")
    cardName=cursor.fetchone()
    if cardName:
        cardName=cardName[0]






    return render_template('edit_profile.html', fName=firstName,lName=lastName,email=email,phoneNum=phoneNumber,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,cardName=cardName)


#update profile information
@app.route('/editprofile', methods = ['GET','POST'])
def updateinfo():
    if request.method == 'POST':

        #edit personal info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']

        #update into dB
        if(firstName!=''):
            statement="UPDATE profile SET firstName='{}' WHERE id=(MAX(id));".format(firstName)
            cursor.execute(statement)
        if(lastName!=''):
            statement="UPDATE profile SET lastName='{}' WHERE id=23".format(lastName)
            cursor.execute(statement)
        if(password!=''):
            statement="UPDATE profile SET phoneNum='{}' WHERE id=23".format(password)
            cursor.execute(statement)
        if(phoneNumber!=''):
            statement="UPDATE profile SET phoneNum='{}' WHERE id=23".format(phoneNumber)
            cursor.execute(statement)

        if(address1!=''):
            statement="UPDATE profile SET address1='{}' WHERE id=23".format(address1)
            cursor.execute(statement)

        if(address2!=''):
            statement="UPDATE profile SET address2='{}' WHERE id=23".format(address2)
            cursor.execute(statement)

        if(zipcode!=''):
            statement="UPDATE profile SET zipcode='{}' WHERE id=23".format(zipcode)
            cursor.execute(statement)

        if(city!=''):
            statement="UPDATE profile SET city='{}' WHERE id=23".format(city)
            cursor.execute(statement)

        if(state!=''):
            statement="UPDATE profile SET state='{}' WHERE id=23".format(state)
            cursor.execute(statement)


        con.commit()

        return redirect(url_for('displayinfo'))
    return render_template('edit_profile.html')






if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)
