from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
from models import db, User, Expense

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and/or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id=current_user.id).all()
    total_expenses = sum(exp.amount for exp in expenses)
    balance = current_user.monthly_income - total_expenses  # Calculate balance

    # Pass `datetime` to the template
    return render_template('dashboard.html', 
                           expenses=expenses, 
                           total_expenses=total_expenses, 
                           balance=balance, 
                           datetime=datetime)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = datetime.now()
        
        # Save the expense with the selected category
        expense = Expense(name=name, amount=amount, category=category, date=date, user_id=current_user.id)
        db.session.add(expense)
        db.session.commit()
        
        flash(f"Expense '{name}' added!", 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')


@app.route('/set_income', methods=['GET', 'POST'])
@login_required
def set_income():
    if request.method == 'POST':
        income = request.form.get('income')
        if income and float(income) >= 0:
            current_user.monthly_income = float(income)
            current_user.update_balance()  # Update balance after setting income
            db.session.commit()
            flash('Monthly income updated!', 'success')
        else:
            flash('Invalid income amount!', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('set_income.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
 