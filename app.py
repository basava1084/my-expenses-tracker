# app.py for running the Personal Expense Tracker UI

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
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')
        
        if not amount or not category:
            return "Amount and Category are required", 400
        
        expenses = load_expenses()
        expenses.append({'amount': float(amount), 'category': category, 'date': date})
        save_expenses(expenses)
        return redirect(url_for('index'))
    
    return '''
    <html><body>
    <h2>Add Expense</h2>
    <form method="post">
        Amount: <input type="number" step="0.01" name="amount" required><br>
        Category: <input type="text" name="category" required><br>
        Date: <input type="date" name="date"><br>
        <input type="submit" value="Add">
    </form>
    <a href="/">Back</a>
    </body></html>
    '''

@app.route('/summary')
def summary():
    expenses = load_expenses()
    total = sum(e['amount'] for e in expenses)
    by_category = defaultdict(float)
    for e in expenses:
        by_category[e['category']] += e['amount']

    summary_html = f"""
    <html><body>
    <h2>Summary</h2>
    <p><strong>Total Spending:</strong> ₹{total}</p>
    <h3>Spending by Category:</h3>
    """
    for category, amount in by_category.items():
        summary_html += f"<p><strong>{category}:</strong> ₹{amount}</p>"
    summary_html += '<a href="/">Back</a></body></html>'
    return summary_html

if __name__ == '__main__':
    app.run(debug=True)
