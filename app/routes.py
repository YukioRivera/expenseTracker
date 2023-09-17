from flask import Blueprint, render_template, request
from datetime import datetime
from app.models import Expense


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
