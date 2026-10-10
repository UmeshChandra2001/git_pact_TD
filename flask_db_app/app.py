from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# --- MySQL Database Configurations ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'          # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'your_password' # Replace with your MySQL password
app.config['MYSQL_DB'] = 'flask_test_db'     # Replace with your Database name

mysql = MySQL(app)

# Helper function to create table on startup
def init_db():
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL
            )
        ''')
        mysql.connection.commit()
        cursor.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from form submission
        name = request.form['name']
        email = request.form['email']

        # Insert data into MySQL database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('index'))

    # Fetch all records to display on the webpage
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    cursor.close()

    return render_template('index.html', users=data)

if __name__ == '__main__':
    init_db()  # Initialize the table
    app.run(debug=True)
