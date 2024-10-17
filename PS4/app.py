from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Database connection
def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="adet"
        )
        return db
    except mysql.connector.Error as err:
        flash(f"Error connecting to the database: {err}", "danger")
        return None

@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login as the first landing page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        contact_number = request.form['contact_number']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']


        # Encrypt the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Get DB connection
        db = get_db_connection()
        if db is None:
            return redirect(url_for('register'))  # If DB connection fails, flash and redirect

        cursor = db.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            flash("This email is already registered. Please log in.", "warning")
            return redirect(url_for('login'))  # Redirect to login if user already exists

        cursor.execute("INSERT INTO adet_user (first_name, middle_name, last_name, contact_number, email, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (first_name, middle_name, last_name, contact_number, email, address, hashed_password))
        db.commit()
        cursor.close()
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Encrypt the password to compare
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Get DB connection
        db = get_db_connection()
        if db is None:
            return redirect(url_for('login'))  # If DB connection fails, flash and redirect

        cursor = db.cursor()
        cursor.execute("SELECT * FROM adet_user WHERE email = %s AND password = %s", (email, hashed_password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]  # Assuming user ID is the first column
            session['first_name'] = user[1]  # Assuming first name is the second column
            return redirect(url_for('dashboard'))
        else:
            flash("Login Failed! Please check your credentials.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("You must log in to view the dashboard.", "warning")
        return redirect(url_for('login'))

    # Get DB connection
    db = get_db_connection()
    if db is None:
        return redirect(url_for('login'))  # If DB connection fails, flash and redirect

    cursor = db.cursor()
    cursor.execute("SELECT first_name, last_name, email FROM adet_user WHERE id = %s", (session['user_id'],))
    user_details = cursor.fetchone()
    cursor.close()

    return render_template('dashboard.html', first_name=user_details[0], user_details=user_details)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)