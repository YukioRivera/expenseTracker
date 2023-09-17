from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.models import Expense
from app import db



main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    amount = request.form.get('amount')
    category = request.form.get('category').lower()
    date_time = datetime.now()

    # Insert data into the database
    expense = Expense(amount=amount, category=category, date_time=date_time)
    db.session.add(expense)
    db.session.commit()

    return redirect(url_for('main.index'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Handle the data entry logic here as you did before
        pass

    desired_month = request.args.get('month', default=current_month)  # You can set a default to the current month

    # Execute the SQL query
    query = """
    SELECT date, amount, category 
    FROM expenses 
    WHERE MONTH(date) = %s
    ORDER BY date ASC;
    """
    expenses = db.execute(query, desired_month).fetchall()

    # Calculate totals and percentages
    total = sum(expense['amount'] for expense in expenses)
    category_totals = {}
    for expense in expenses:
        if expense['category'] not in category_totals:
            category_totals[expense['category']] = 0
        category_totals[expense['category']] += expense['amount']

    category_percentages = {category: (amount / total) * 100 for category, amount in category_totals.items()}

    # Pass the data to the template
    return render_template('home.html', expenses=expenses, total=total, category_percentages=category_percentages)
