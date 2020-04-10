from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "Clear1998"
app.config['MYSQL_DATABASE_DB'] = "bookstore"
app.config['MYSQL__DATABASE_HOST'] = "localhost"
mysql = MySQL(app)

con = mysql.connect()
cursor=con.cursor()

#this app.route is specific to register page

@app.route('/', methods = ['GET','POST'])
def index():
    return render_template('homepage.html')

@app.route('/main', methods = ['GET','POST'])
def main():
    return render_template('main.html')

@app.route('/account_verification', methods = ['GET','POST'])
def verify():
    return render_template('account_verification.html')

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
        ccv = request.form['ccv']
        expirationDate = request.form['expirationDate']

        #store into dB
        cursor.execute("INSERT INTO profile(firstName, lastName, email, pswd, phoneNum, shippingAddress) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, lastName, email, password, phoneNumber, shipAdd))
        cursor.execute("INSERT INTO paymentMethod(name, type, cardNumber, expirationDate, ccv) VALUES (%s,%s,%s,%s,%s)", (name, cardType, cardNumber, expirationDate, ccv))



        #get payment info
        name = request.form['name']
        cardType = request.form['cardType']
        cardNumber = request.form['cardNumber']
        ccv = request.form['ccv']
        expirationDate = request.form['expirationDate']

        #store into dB
        cursor.execute("INSERT INTO profile(firstName, lastName, email, pswd, phoneNum, shippingAddress) VALUES (%s,%s,%s,%s,%s,%s)", (firstName, lastName, email, password, phoneNumber, shipAdd))
        cursor.execute("INSERT INTO paymentMethod(name, type, cardNumber, expirationDate, ccv) VALUES (%s,%s,%s,%s,%s)", (name, cardType, cardNumber, expirationDate, ccv))

        con.commit()


        return redirect(url_for('verify'))
    return render_template('registration.html')

#login function
@app.route('/login/', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        #get personal info
        return render_template("login.html",error=False)

    if request.form['email']!="email@gmail.com" or request.form['password']!= "password":
        return render_template('login.html',error = True)

    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)


