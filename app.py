from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_session import Session
from cryptography.fernet import Fernet
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# In-memory storage for users and passwords
users = {'admin': 'admin123'}  # username 'admin', password 'admin123'
passwords_file = 'passwords.json'
key_file = 'secret.key'

# Function to generate a key and save it to a file
def generate_key():
    global key_file  # Declare key_file as global
    key = Fernet.generate_key()
    with open(key_file, 'wb') as kf:
        kf.write(key)

# Function to load the key from a file
def load_key():
    return open(key_file, 'rb').read()

# Function to encrypt data
def encrypt_data(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt_data(encrypted_data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to load passwords from file
def load_passwords():
    if not os.path.exists(passwords_file):
        return []

    with open(passwords_file, 'rb') as file:
        encrypted_data = file.read()

    decrypted_data = decrypt_data(encrypted_data)
    return json.loads(decrypted_data)

# Function to save passwords to file
def save_passwords(passwords):
    encrypted_data = encrypt_data(json.dumps(passwords))
    with open(passwords_file, 'wb') as file:
        file.write(encrypted_data)

# Generate a key if it doesn't exist
if not os.path.exists(key_file):
    generate_key()

# Load passwords at startup
passwords = load_passwords()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', passwords=passwords)

@app.route('/add_password', methods=['POST'])
def add_password():
    if 'username' not in session:
        return redirect(url_for('login'))

    owner = request.form['owner']
    site = request.form['site']
    password = request.form['password']

    # Append a dictionary with owner, site, and password
    passwords.append({'owner': owner, 'site': site, 'password': password})

    # Save updated passwords to file
    save_passwords(passwords)

    flash(f'Password for {site} added successfully!')
    return redirect(url_for('dashboard'))

@app.route('/remove_password/<int:index>')
def remove_password(index):
    if 'username' not in session:
        return redirect(url_for('login'))

    if 0 <= index < len(passwords):
        del passwords[index]
        # Save updated passwords to file after deletion
        save_passwords(passwords)
        flash(f'Password removed successfully!')

    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
