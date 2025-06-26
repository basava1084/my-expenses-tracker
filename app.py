# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
DATA_FILE = 'expenses.json'

def load_expenses():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

@app.route('/')
def index():
    expenses = load_expenses()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date'] or datetime.now().strftime('%Y-%m-%d')

        expenses = load_expenses()
        expenses.append({'amount': amount, 'category': category, 'date': date})
        save_expenses(expenses)

        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/summary')
def summary():
    expenses = load_expenses()
    total = sum(e['amount'] for e in expenses)
    by_category = defaultdict(float)
    for e in expenses:
        by_category[e['category']] += e['amount']

    return render_template('summary.html', total=total, by_category=by_category)

if __name__ == '__main__':
    app.run(debug=True)
