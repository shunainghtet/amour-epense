from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    monthly_income = db.Column(db.Float, default=0.0)
    balance = db.Column(db.Float, default=0.0)  # Store balance

    def __repr__(self):
        return f"<User {self.username}>"

    def update_balance(self):
        """Update the balance based on income and expenses."""
        expenses = Expense.query.filter_by(user_id=self.id).all()
        total_expenses = sum(exp.amount for exp in expenses)
        self.balance = self.monthly_income - total_expenses
        db.session.commit()


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.name}, {self.amount}>"
