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
@app.route('/')
def displayinfo():
    cursor.execute("SELECT id,firstName,lastName,email FROM profile")

    data=cursor.fetchall()

    print(data)
    return render_template('edit_profile.html', user=data)

if __name__ == '__main__':
    app.run(debug=True)



#inputName = "Patrick"

#get = getSQLProcessor.getSQLProcessor()
#age = get.getCredentials("Patrick")

#print(age)
