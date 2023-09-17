from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import Expense
from app import db

main = Blueprint('main', __name__)

@main.route('/submit', methods=['POST'])
def submit():
    amount = float(request.form.get('amount'))
    category = request.form.get('category').lower()
    date_time = datetime.now()

    # Insert data into the database
    expense = Expense(amount=amount, category=category, date_time=date_time)
    # this was added check this if the website doesnt work 
    try:
        db.session.add(expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('main.home'))

@main.route('/', methods=['GET', 'POST'])
def home():
    desired_date = request.args.get('date', default=datetime.now().strftime('%Y-%m'))
    year, month = map(int, desired_date.split('-'))

    # Execute the SQL query
    expenses = Expense.query.filter(db.extract('year', Expense.date_time) == year, db.extract('month', Expense.date_time) == month).all()
    print("expenses: ", expenses)
    
    # Calculate totals and percentages
    print("sum(expense.amount for expense in expenses): ", sum(expense.amount for expense in expenses))
    total = sum(expense.amount for expense in expenses)
    category_totals = {}
    for expense in expenses:
        print(f"expenses: ", expense)
        print(f"expense.category: ", expense.category)
        print("expense.category not in category_totals", expense.category not in category_totals)
        if expense.category not in category_totals:
            category_totals[expense.category] = 0
        category_totals[expense.category] += expense.amount

    category_percentages = {category: round((amount / total) * 100, 2) for category, amount in category_totals.items()}

    print("category_totals: {category_totals}")

    return render_template('index.html', expenses=expenses, total=total, category_percentages=category_percentages, desired_date=desired_date, category_totals=category_totals)
