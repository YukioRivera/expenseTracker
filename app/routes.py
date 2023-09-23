from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import Expense
from app import db
from collections import defaultdict
from flask import jsonify


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
    # print("expenses: ", expenses)
    
    # Calculate totals and percentages
    # print("sum(expense.amount for expense in expenses): ", sum(expense.amount for expense in expenses))
    total = sum(expense.amount for expense in expenses)
    category_totals = {}
    for expense in expenses:
        # print(f"expenses: ", expense)
        # print(f"expense.category: ", expense.category)
        # print("expense.category not in category_totals", expense.category not in category_totals)
        if expense.category not in category_totals:
            category_totals[expense.category] = 0
        category_totals[expense.category] += expense.amount

    category_percentages = {category: round((amount / total) * 100, 2) for category, amount in category_totals.items()}
    # print("category_totals: {category_totals}")

    return render_template('index.html', expenses=expenses, total=total, category_percentages=category_percentages, desired_date=desired_date, category_totals=category_totals)

@main.route('/expense_insights', methods=['GET'])
def expense_insights():
    # Fetch all expenses
    all_expenses = Expense.query.order_by(Expense.date_time).all()

    # Organize expenses by month
    expenses_by_month = defaultdict(list)
    for expense in all_expenses:
        month_year_key = expense.date_time.strftime('%B %Y')  # e.g., "September 2023"
        expenses_by_month[month_year_key].append(expense)
    
    # print("expenses_by_month: ", expenses_by_month)
    return render_template('expense_insights.html', expenses_by_month=expenses_by_month)

@main.route('/update-entry', methods=['POST'])
def update_entry():
    data = request.json
    print("data", data)
    entry_id = data['id']
    date = data['date']
    time = data['time']
    category = data['category']
    amount = data['amount']
    entry = Expense.query.get(entry_id)
    if entry:
        entry.date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
        entry.category = category
        entry.amount = float(amount)  # Convert string to float
        db.session.commit()
        return {"success": True}, 200
    return {"success": False, "message": "Entry not found"}, 404

@main.route('/remove-entry', methods=['POST'])
def remove_entry():
    data = request.get_json()
    entry_id = data.get('id')
    
    entry = Expense.query.get(entry_id)
    if entry:
        try:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)})
    else:
        return jsonify({'success': False, 'message': 'Entry not found'}), 404

@main.route('/update-entries', methods=['POST'])
def update_entries():
    entries = request.json.get('entries', [])
    try:
        for entry_data in entries:
            entry_id = entry_data['id']
            date = entry_data['date']
            time = entry_data['time']
            category = entry_data['category']
            amount = entry_data['amount']
            entry = Expense.query.get(entry_id)
            if entry:
                entry.date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
                entry.category = category
                entry.amount = float(amount)  # Convert string to float
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
