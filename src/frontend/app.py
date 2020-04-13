from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "whatWhat11"
app.config['MYSQL_DATABASE_DB'] = "csci4050_bookstore"
app.config['MYSQL__DATABASE_HOST'] = "localhost"
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

#goes to this after submitting registration info
@app.route('/account_verification', methods = ['GET','POST'])
def verify():
    return render_template('account_verification.html')

#register function
@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        #get personal info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']


        #get payment info
        name = request.form['name']
        cardType = request.form['cardType']
        cardNumber = request.form['cardNumber']
        expirationDate = request.form['expirationDate']
        shippingAddress = request.form['address1'] + request.form['address2'] + request.form['zip'] + request.form['city'] + request.form['state']
        #store into dB
        cursor.execute("INSERT INTO profile(firstName, lastName, phoneNum, email, pswd, shippingAddress) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, lastName, phoneNumber, email, password, shippingAddress))
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
        if inputEmail == email and inputPass ==passWord:
            isUser = True

    if isUser == False:
        return render_template("login.html")
    return redirect(url_for('main'))
 #   if request.method == 'GET':
        #get personal info
   #     return render_template("login.html",error=False)

 #   if request.form['email']!="email@gmail.com" or request.form['password']!= "password":
   #     return render_template('login.html',error = True)

    return render_template("login.html")



if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)
