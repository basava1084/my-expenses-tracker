from flask import Flask, render_template, request, redirect, url_for, flash, session
import json, os
from datetime import datetime
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_expenses(email):
    file = f'expenses_{email}.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_expenses(email, expenses):
    file = f'expenses_{email}.json'
    with open(file, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        users[email] = generate_password_hash(password)
        save_users(users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and check_password_hash(users[email], password):
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        users = load_users()
        if email in users:
            session['reset_email'] = email
            flash('Email found. Please enter your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Email not registered.', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        flash('Please use Forgot Password to initiate reset.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        users = load_users()
        users[session['reset_email']] = generate_password_hash(new_password)
        save_users(users)
        session.pop('reset_email', None)
        flash('Password reset successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    total = sum(float(e['amount']) for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        expenses = load_expenses(session['email'])
        expenses.append({'amount': amount, 'category': category, 'date': date})
        save_expenses(session['email'], expenses)
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete_expense(index):
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(session['email'], expenses)
        flash('Expense deleted successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    summary_by_category = defaultdict(float)
    total = 0
    for e in expenses:
        amount = float(e['amount'])
        summary_by_category[e['category']] += amount
        total += amount
    return render_template('summary.html', summary=summary_by_category, total=total)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json, os
from datetime import datetime
from collections import defaultdict
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def load_expenses(email):
    file = f'expenses_{email}.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_expenses(email, expenses):
    file = f'expenses_{email}.json'
    with open(file, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users:
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        users[email] = generate_password_hash(password)
        save_users(users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()
        if email in users and check_password_hash(users[email], password):
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        users = load_users()
        if email in users:
            session['reset_email'] = email
            flash('Email found. Please enter your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Email not registered.', 'error')
            return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        flash('Please use Forgot Password to initiate reset.', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        users = load_users()
        users[session['reset_email']] = generate_password_hash(new_password)
        save_users(users)
        session.pop('reset_email', None)
        flash('Password reset successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

@app.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    total = sum(float(e['amount']) for e in expenses)
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')
        expenses = load_expenses(session['email'])
        expenses.append({'amount': amount, 'category': category, 'date': date})
        save_expenses(session['email'], expenses)
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:index>')
def delete_expense(index):
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    if 0 <= index < len(expenses):
        expenses.pop(index)
        save_expenses(session['email'], expenses)
        flash('Expense deleted successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    if 'email' not in session:
        return redirect(url_for('login'))
    expenses = load_expenses(session['email'])
    summary_by_category = defaultdict(float)
    total = 0
    for e in expenses:
        amount = float(e['amount'])
        summary_by_category[e['category']] += amount
        total += amount
    return render_template('summary.html', summary=summary_by_category, total=total)

if __name__ == '__main__':
    app.run(debug=True)
