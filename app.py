from flask import Flask, request, jsonify, make_response
import sqlite3

app = Flask(__name__)

# Initialize the database (for demonstration purposes)
def init_db():
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    
    # Drop the existing users table if it exists to ensure a fresh start
    c.execute('''DROP TABLE IF EXISTS users''')
    
    # Create the users table anew
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)''')
    
    # Insert the specified user accounts
    user_accounts = [
        ('Kenneth Cher', 1000),
        ('Bill Luong', 1000),
        ('Jessica Leung', 1000),
        ('Derrick Tran', 1000),
        ('Tyranno Rex', 1000), ('Stego Sarah', 1000), ('Veloci Raptor', 1000),
        ('Bronto Bill', 1000), ('Tricera Tops', 1000), ('Ankylo Andy', 1000),
        ('Ptero Peter', 1000), ('Diplo Dan', 1000), ('Iguano Izzy', 1000),
        ('Mammothus Maximus', 1000)
    ]
    
    # Insert all user accounts in a single operation
    c.executemany('''INSERT INTO users (name, balance) VALUES (?, ?)''', user_accounts)
    
    conn.commit()
    conn.close()

init_db()

# SQL Injection
@app.route('/login', methods=['POST'])
def login():
    
    username = request.form['username']
    password = request.form['password']
    
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

# Broken Object Level Authorization
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