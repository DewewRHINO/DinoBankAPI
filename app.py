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
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, password TEXT, balance INTEGER, age INTEGER)''')
    
    # Insert the specified user accounts///////////////////////////////////////////////////////could use sql injection to get pass potentially
    user_accounts = [
        ('Admin', 'superYuh', 1000, 20),
        ('Kenneth Cher', 'yuh', 1000, 20),
        ('Bill Luong', 'yuh', 1000, 21),
        ('Jessica Leung', 'yuh', 1000, 22),
        ('Derrick Tran', 'yuh', 1000, 52),
        ('Tyranno Rex', 'yuh', 1000, 21), ('Stego Sarah', 'yuh', 1000, 65), ('Veloci Raptor', 'yuh', 1000, 49),
        ('Bronto Bill', 'yuh', 1000, 43), ('Tricera Tops', 'yuh', 1000, 24), ('Ankylo Andy', 'yuh', 1000, 33),
        ('Ptero Peter', 'yuh', 1000, 22), ('Diplo Dan', 'yuh', 1000, 39), ('Iguano Izzy', 'yuh', 1000, 53),
        ('Mammothus Maximus', 'yuh', 1000, 18)
    ]
    
    # Insert all user accounts in a single operation
    c.executemany('''INSERT INTO users (name, password, balance, age) VALUES (?, ?, ?, ?)''', user_accounts)
    
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
    
# Create Account
@app.route('/account', methods=['POST'])
def create_account():
    # Parse request data
    data = request.json
    username = data.get('username')
    password = data.get('password')
    balance = 1000
    age = data.get('age')
    
    # Perform validation
    if not username or not password or not age:
        return jsonify({"message": "Username, password, and age are required"}), 400
    
    # Check if the username is already taken ///////////////////////////////////////////if no input validation potential challenge
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (username,))
    if c.fetchone():
        conn.close()
        return jsonify({"message": "Username already exists"}), 409
    
    # Insert new user record
    c.execute("INSERT INTO users (name, password, balance, age) VALUES (?, ?, ?, ?)", (username, password, balance, age))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Account created successfully"}), 201

# Broken Object Level Authorization
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({"id": user[0], "name": user[1], "balance": user[3], "age": user[4]}), 200
    else:
        return jsonify({"message": "User not found"}), 404

# Information endpoint
@app.route('/information', methods=['GET'])
def information():
    return 'Dinobank. Protecting your assets since 65 MYA.\n'

# Deposit Endpoint
@app.route('/account/deposit', methods=['POST'])
def deposit():
    data = request.json
    username = data.get('username')
    amount = data.get('amount')
    
    if not username or not amount:
        return jsonify({"message": "Username and amount are required"}), 400

    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = c.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"message": "User not found"}), 404
    
    new_balance = user[3] + amount
    c.execute("UPDATE users SET balance = ? WHERE name = ?", (new_balance, username))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "woo hoo youre rich", "new_balance": new_balance}), 200

# Withdraw Endpoint
@app.route('/account/withdraw', methods=['POST'])
def withdraw():
    data = request.json
    username = data.get('username')
    amount = data.get('amount')
    
    if not username or not amount:
        return jsonify({"message": "Username and amount are required"}), 400

    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (username,))
    user = c.fetchone()
    
    if not user:
        conn.close()
        return jsonify({"message": "User not found"}), 404
    
    if user[3] < amount:
        conn.close()
        return jsonify({"message": "Insufficient balance"}), 403
    
    new_balance = user[3] - amount
    c.execute("UPDATE users SET balance = ? WHERE name = ?", (new_balance, username))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "womp womp gotta spend some to make some", "new_balance": new_balance}), 200

# Account Endpoint
@app.route('/users', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    user_list = []
    for user in users:
        user_list.append({"id": user[0], "name": user[1], "balance": user[3], "age": user[4]})
    return jsonify(user_list), 200

# Delete user (admin only) ///////////////////////////////////////need login token to work

@app.route('/user/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('dinobank.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "User deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)



