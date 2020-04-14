from flask import Flask, render_template, request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = "root"
app.config['MYSQL_DATABASE_PASSWORD'] = "whatWhat11"
app.config['MYSQL_DATABASE_DB'] = "bookstore"
app.config['MYSQL__DATABASE_HOST'] = "localhost"
mysql = MySQL(app)

con = mysql.connect()
cursor=con.cursor()
@app.route('/')
def displayinfo():
    cursor.execute("SELECT firstName FROM profile WHERE id=23;")
    firstName=cursor.fetchall()

    cursor.execute("SELECT lastName FROM profile WHERE id=23;")
    lastName=cursor.fetchall()

    cursor.execute("SELECT email FROM profile WHERE id=23;")
    email=cursor.fetchall()

    cursor.execute("SELECT phoneNum FROM profile WHERE id=23;")
    phoneNumber=cursor.fetchall()


    return render_template('edit_profile.html', fName=firstName,lName=lastName,email=email,phoneNum=phoneNumber)

#register function
@app.route('/', methods = ['GET','POST'])
def updateinfo():
    if request.method == 'POST':

        #edit personal info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        password = request.form['password']
        phoneNumber = request.form['phoneNumber']









        #update into dB
        if(firstName!=''):
            statement="UPDATE profile SET firstName={} WHERE id=23".format(firstName)
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



        con.commit()

        return redirect(url_for('displayinfo'))
    return render_template('edit_profile.html')

if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)
