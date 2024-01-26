import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('login.db')
#database
cursor = conn.cursor()

# Create users table if not exists - database creation
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        age INTEGER,    
        email TEXT
    )
''')
conn.commit()

# Insert user function - database changes
# database interaction with API
def insert_user(username, password, age, email):
    cursor.execute('''
        INSERT INTO users (username, password, age, email)
        VALUES (?, ?, ?, ?)
    ''', (username, password, age, email))
    conn.commit()

# Get all users function - data retrieval
# database interaction with API
def get_all_users():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

# API endpoint to insert a user
@app.route('/insert_user', methods=['POST'])
def api_insert_user():
    data = request.json
    insert_user(data['username'], data['password'], data['age'], data['email'])
    return jsonify({'message': 'User inserted successfully'})

# API endpoint to get all users
@app.route('/get_all_users', methods=['GET'])
def api_get_all_users():
    users = get_all_users()
    return jsonify({'users': users})

# Close the connection when the app shuts down
@app.teardown_appcontext
def close_connection(exception):
    conn.close()

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
