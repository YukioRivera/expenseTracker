from datetime import datetime
from app import db
from flask_login import UserMixin

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.id} - {self.amount} - {self.category} - {self.date_time}>"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
