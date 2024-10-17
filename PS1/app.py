from flask import Flask, render_template, request, redirect, url_for
import mysql.connector  

app = Flask(__name__)


db_config = {
    'user': 'your_username',      
    'password': 'your_password',   
    'host': 'localhost',          
    'database': 'adet'             
}


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': 
       
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        cnum = request.form['cnum']
        email = request.form['email']
        address = request.form['address']

        
        try:
            
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            
            query = """
            INSERT INTO adet_user (fname, mname, lname, cnum, email, address) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fname, mname, lname, cnum, email, address))
            
            
            conn.commit()
            
            
            cursor.close()
            conn.close()
            
            
            return redirect(url_for('success'))
        except mysql.connector.Error as err:
           
            print(f"Error: {err}")
            return "Database connection error"

    
    return render_template('register.html')


@app.route('/success')
def success():
    return "Registration successful!"

if __name__ == '__main__':
    
    app.run(debug=True)
