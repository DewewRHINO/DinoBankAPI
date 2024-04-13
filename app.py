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
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER, age INTEGER)''')
    
    # Insert the specified user accounts
    user_accounts = [
        ('Kenneth Cher', 1000, 20),
        ('Bill Luong', 1000, 21),
        ('Jessica Leung', 1000, 22),
        ('Derrick Tran', 1000, 52),
        ('Tyranno Rex', 1000, 21), ('Stego Sarah', 1000, 65), ('Veloci Raptor', 1000, 49),
        ('Bronto Bill', 1000, 43), ('Tricera Tops', 1000, 24), ('Ankylo Andy', 1000, 33),
        ('Ptero Peter', 1000, 22), ('Diplo Dan', 1000, 39), ('Iguano Izzy', 1000, 53),
        ('Mammothus Maximus', 1000, 18)
    ]
    
    # Insert all user accounts in a single operation
    c.executemany('''INSERT INTO users (name, balance, age) VALUES (?, ?, ?)''', user_accounts)
    
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
        return jsonify({"id": user[0], "name": user[1], "balance": user[2], "age": user[3]}), 200
    else:
        return jsonify({"message": "User not found"}), 404

#info endpoint
@app.route('/information', methods=['GET'])
def information():
    return 'Dinobank. Protecting your assets since 65 MYA.\n'





if __name__ == '__main__':
    app.run(debug=True)



