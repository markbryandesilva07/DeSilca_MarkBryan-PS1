from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import mysql.connector.errorcode

app = Flask(__name__)

try:
    conn=mysql.connector.connect(
        user="root",
        host="localhost",
        database="adet"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        conn=mysql.connector.connect(
            user="root",
            host="localhost"
        )
        cursor = conn.cursor()
        cursor.execute("create database adet")
        cursor.execute("use adet")
        cursor.execute(
            "create table users ("
            " id INT(11) NOT NULL auto_increment,"
            " firstname VARCHAR(255) NOT NULL,"
            " middlename VARCHAR(255) NOT NULL,"
            " lastname VARCHAR(255) NOT NULL,"
            " contactnumber VARCHAR(11) NOT NULL,"
            " email VARCHAR(255) NOT NULL,"
            " address VARCHAR(255) NOT NULL,"
            " primary key(id)"
            ")"
            )



@app.route('/', methods=['GET', 'POST'])
def home():
    user = request.cookies.get("user")
    if user == None:
        return redirect(url_for("register"))
    
    return render_template("greeting.html", name = user)

@app.route('/register', methods=['GET'])
def register():
    return render_template("form.html")


@app.route('/submit', methods=['POST'])
def submit():
    firstname=request.form.get("fname")
    middlename=request.form.get("mname")
    lastname=request.form.get("lname")
    contactnum=request.form.get("cnum")
    email=request.form.get("email")
    address=request.form.get("address")
    
    query = "insert into users values (NULL, %s, %s, %s, %s, %s, %s)"
    val = (firstname, middlename, lastname, contactnum, email, address)
    cursor.execute(query,val)
    conn.commit()

    req = redirect(url_for("home"))
    req.set_cookie("user", firstname)
    
    return req

if __name__ == '__main__':
    app.run(debug=True)
