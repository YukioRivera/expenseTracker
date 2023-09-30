from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import Expense, User, RecurringCharge
from app import db, login_manager
from collections import defaultdict
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user


main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))  # Redirect to index.html page

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.login'))

@main.route('/', methods=['GET', 'POST'])
@login_required
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
    
    # Get the list of unique categories that have recurring charges
    recurring_categories = db.session.query(RecurringCharge.category).distinct().all()
    print("recurring_categories: ", recurring_categories)
    recurring_category_names = [category[0] for category in recurring_categories]
    print("recurring_category_names: ", recurring_category_names)

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        category_percentages=category_percentages,
        desired_date=desired_date,
        category_totals=category_totals,  # Ensure there's a comma here
        recurring_category_names=recurring_category_names  # pass the data to the template
    )

@main.route('/expense_insights', methods=['GET'])
@login_required
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

@main.route('/submit', methods=['POST'])
@login_required
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

@main.route('/update-entry', methods=['POST'])
@login_required
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
@login_required
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
@login_required
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

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             # Login successful, redirect to index page
#             return redirect(url_for('main.index'))
#         else:
#             # Login failed, show error message
#             error_message = "Invalid username or password. Please try again."
#             return render_template('login.html', error_message=error_message)
#     return render_template('login.html')

@main.route('/add-recurring', methods=['POST'])
@login_required
def add_recurring():
    amount = float(request.form.get('amount'))
    category = request.form.get('category').lower()
    start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d").date()
    end_date_str = request.form.get('end_date')
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
    day_of_month = int(request.form.get('day_of_month'))
    user_id = current_user.id  # Assuming you have Flask-Login setup

    # Create a new RecurringCharge object
    recurring_charge = RecurringCharge(
        amount=amount,
        category=category,
        start_date=start_date,
        end_date=end_date,
        day_of_month=day_of_month,
        user_id=user_id
    )

    # Insert data into the database
    try:
        db.session.add(recurring_charge)
        db.session.commit()
        flash('Recurring charge added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('main.home'))
