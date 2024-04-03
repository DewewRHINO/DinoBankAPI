from flask import Flask, request, jsonify, make_response
import sqlite3

app = Flask(__name__)

# Initialize the database (for demonstration purposes)
def init_db():
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)''')
    c.execute('''INSERT INTO users (name, balance) VALUES ('Kenneth Cher', 1000)''')
    c.execute('''INSERT INTO users (name, balance) VALUES ('Bill Luong', 1000)''')
    c.execute('''INSERT INTO users (name, balance) VALUES ('Jessica Leung', 1000)''')
    conn.commit()
    conn.close()

init_db()

# Vulnerable to SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print (f"This is the username {username}. This is the password {password}")
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{username}' AND password = '{password}'"
    c.execute(query) # Vulnerable line
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"message": "Login successful", "user": user[1]}), 200
    else:
        return jsonify({"message": "Login failed"}), 401

# Vulnerable to Broken Object Level Authorization
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "balance": user[2]}), 200
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
