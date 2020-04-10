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
@app.route('/', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']

        cursor.execute("INSERT INTO profile(firstName, lastName, email, pswd, phoneNum) VALUES (%s,%s,%s,%s,%s)", (firstName, lastName, email, password, phoneNumber))
        status=0
        verificationCode=""
        cursor.execute("INSERT INTO registeredUser(status,verificationCode) VALUES (%s,%s)", (status,verificationCode))
        con.commit()
        cursor.close()
        return 'success'
    return render_template('edit_profile.html')

if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)
