from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from app.models import Expense, User, RecurringCharge
from app import db, login_manager
from collections import defaultdict
from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import logging

logging.basicConfig(level=logging.INFO)


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

    # Execute the SQL query for Expenses
    expenses = Expense.query.filter(db.extract('year', Expense.date_time) == year, db.extract('month', Expense.date_time) == month).all()
    
    # Query the RecurringCharge table
    recurring_charges = RecurringCharge.query.filter_by(user_id=current_user.id).all()

    # Step 1: Create a Unified Data Structure
    unified_data = []
    for expense in expenses:
        unified_data.append({
            'category': expense.category.strip(),
            'amount': expense.amount,
            'type': 'Expense'
        })

    # Get the first and last day of the desired month
    first_day_of_month = datetime(year, month, 1).date()  # Convert to datetime.date object
    last_day_of_month = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1).date() - timedelta(days=1)  # Convert to datetime.date object

    for recurring_charge in recurring_charges:
        # Check if the recurring charge is active for the desired month
        if (recurring_charge.start_date <= last_day_of_month and
            (recurring_charge.end_date is None or recurring_charge.end_date >= first_day_of_month)):
            # Ensure the day of the month does not exceed the last day of the month
            day_of_month = min(recurring_charge.day_of_month, last_day_of_month.day)
            # Calculate the date of the recurring charge for the desired month
            recurring_date = datetime(year, month, day_of_month).date()  # Convert to datetime.date object
            # Ensure the date is within the start and end dates of the recurring charge
            if recurring_charge.start_date <= recurring_date and (recurring_charge.end_date is None or recurring_charge.end_date >= recurring_date):
                unified_data.append({
                    'category': recurring_charge.category.strip(),
                    'amount': recurring_charge.amount,
                    'type': 'Recurring Charge'
                })

    # Step 2: Aggregate the Data by Category
    aggregated_data = defaultdict(lambda: {'amount': 0, 'type': set()})
    for item in unified_data:
        aggregated_data[item['category']]['amount'] += item['amount']
        aggregated_data[item['category']]['type'].add(item['type'])

    # Convert the aggregated data to a list of dictionaries
    aggregated_data_list = [{
        'category': category,
        'amount': data['amount'],
        'type': ', '.join(data['type'])
    } for category, data in aggregated_data.items()]

    # Step 3: Calculate Percentages
    grand_total = sum(item['amount'] for item in aggregated_data_list)
    for item in aggregated_data_list:
        item['percentage_of_total'] = round((item['amount'] / grand_total) * 100, 2)

    # Step 4: Sort the Data
    sorted_data = sorted(aggregated_data_list, key=lambda x: x['category'])

    # Step 5: Pass the Data to the Template
    return render_template(
        'index.html',
        data=sorted_data,
        grand_total=grand_total,
        desired_date=desired_date
    )


@main.route('/expense_insights', methods=['GET'])
@login_required
def expense_insights():
    # Fetch all expenses
    all_expenses = Expense.query.order_by(Expense.date_time).all()
    
    # Query the RecurringCharge table
    recurring_charges = RecurringCharge.query.filter_by(user_id=current_user.id).all()

    # Organize expenses by month
    expenses_by_month = defaultdict(list)
    for expense in all_expenses:
        month_year_key = expense.date_time.strftime('%B %Y')  # e.g., "September 2023"
        expenses_by_month[month_year_key].append(expense)
        
    # Organize recurring expenses by month 
    recurring_expenses_by_month = defaultdict(list)
    for recurringCharge in recurring_charges:
        start_date = recurringCharge.start_date.replace(day=1)  # Set to the first day of the month
        end_date = recurringCharge.end_date
        if end_date:
            end_date = datetime(end_date.year, end_date.month, 1)  # Convert to datetime and set to the first day of the month
        else:
            end_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Set to the first day of the current month
        
        # Iterate through each month in the range and add the recurring charge
        current_date = datetime(start_date.year, start_date.month, 1)  # Convert to datetime and set to the first day of the month
        while current_date <= end_date:
            month_year_key = current_date.strftime('%B %Y')
            recurring_expenses_by_month[month_year_key].append(recurringCharge)
            # Move to the first day of the next month
            current_date += timedelta(days=32)
            current_date = current_date.replace(day=1)
    
    # Get all unique months from both expenses and recurring expenses
    all_months = set(expenses_by_month.keys()) | set(recurring_expenses_by_month.keys())
    
    # Sort the months chronologically
    all_months = sorted(list(all_months), key=lambda x: datetime.strptime(x, '%B %Y'))

    return render_template(
        'expense_insights.html', 
        expenses_by_month=expenses_by_month,
        recurring_expenses_by_month=recurring_expenses_by_month,
        all_months=all_months  # Pass the sorted list of all months to the template
    )

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

@main.route('/remove-entry', methods=['POST'])
@login_required
def remove_entry():
    data = request.get_json()
    entry_id = data.get('id')
    is_recurring = data.get('isRecurring', False)
    
    logging.info(f"is_recurring: {is_recurring}")
    if is_recurring:
        entry = RecurringCharge.query.get(entry_id)
    else:
        entry = Expense.query.get(entry_id)
    
    if entry:
        try:
            db.session.delete(entry)
            db.session.commit()
            logging.info("db commit try")
            return jsonify({'success': True})
        except Exception as e:
            db.session.rollback()
            logging.error(f"db commit False, line 220: {str(e)}")
            return jsonify({'success': False, 'message': str(e)})
    else:
        logging.error("db commit false, line 223, 2nd if else")
        return jsonify({'success': False, 'message': 'Entry not found'}), 404

@main.route('/update-entry', methods=['POST'])
@login_required
def update_entry():
    data = request.json
    print("data", data)
    entry_id = data['id']
    date = data['date']
    # time = data['time']
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


@main.route('/update-entries', methods=['POST'])
@login_required
def update_entries():
    logging.info("Entered update_entries function")  # New log statement
    entries = request.json.get('entries', [])
    logging.info(f'Entries to update: {entries}')  # Log the entries payload
    try:
        for entry_data in entries:
            entry_id = entry_data['id']
            date = entry_data['date']
            category = entry_data['category']
            amount = entry_data['amount']
            description = entry_data['description']
            # date_time = entry_data['time']
            entry = Expense.query.get(entry_id)
            if entry:
                entry.description = description  # Set the description
                # entry.date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")  # Convert string to datetime
                entry.category = category
                entry.amount = float(amount)  # Convert string to float
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logging.exception(f'Error updating entries: {e}')  # Log any errors
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

@main.route('/update-recurring-entries', methods=['POST'])
@login_required
def update_recurring_entries():
    data = request.get_json()
    entries = data.get('entries')
    
    for entry in entries:
        recurring_charge = RecurringCharge.query.get(entry['id'])
        recurring_charge.start_date = datetime.strptime(entry['startDate'], '%Y-%m-%d')
        recurring_charge.end_date = datetime.strptime(entry['endDate'], '%Y-%m-%d') if entry['endDate'] != 'N/A' else None
        recurring_charge.category = entry['category']
        recurring_charge.amount = float(entry['amount'])
    
    try:
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=str(e))
