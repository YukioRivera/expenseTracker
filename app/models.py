from datetime import datetime, date
from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import SelectField

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Assuming description is of type String and is nullable
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.id} - {self.amount} - {self.category} - {self.description} - {self.date_time}>"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    recurring_charges = db.relationship('RecurringCharge', backref='user', lazy=True)

class RecurringCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=date.today())
    end_date = db.Column(db.Date, nullable=True)
    day_of_month = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    
class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=True)  # Source of the income
    amount = db.Column(db.Float, nullable=False)
    income_date = db.Column(db.Date, nullable=False, default=date.today())
    recurrence_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Linking income to a user
