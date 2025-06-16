from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User, Transaction
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def home():
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password or not confirm_password:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'danger')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    
    total_income = sum(txn.amount for txn in transactions if txn.type == 'income')
    total_expense = sum(txn.amount for txn in transactions if txn.type == 'expense')
    balance = total_income - total_expense

    return render_template('dashboard.html', transactions=transactions,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

@main.route('/add', methods=['POST'])
@login_required
def add_transaction():
    title = request.form.get('title', '').strip()
    amount_str = request.form.get('amount', '0').strip()
    txn_type = request.form.get('type', '').strip()
    category = request.form.get('category', '').strip()

    if not title or not amount_str or not txn_type or not category:
        flash('Please fill in all fields to add a transaction.', 'danger')
        return redirect(url_for('main.dashboard'))

    try:
        amount = float(amount_str)
    except ValueError:
        flash('Amount must be a valid number.', 'danger')
        return redirect(url_for('main.dashboard'))

    if amount <= 0:
        flash('Amount must be greater than zero.', 'danger')
        return redirect(url_for('main.dashboard'))

    if txn_type not in ['income', 'expense']:
        flash('Transaction type must be "income" or "expense".', 'danger')
        return redirect(url_for('main.dashboard'))

    new_txn = Transaction(
        title=title,
        amount=amount,
        type=txn_type,
        category=category,
        user_id=current_user.id
    )
    db.session.add(new_txn)
    db.session.commit()
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/edit/<int:txn_id>', methods=['GET', 'POST'])
@login_required
def edit_transaction(txn_id):
    txn = Transaction.query.get_or_404(txn_id)

    if txn.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        amount_str = request.form.get('amount', '0').strip()
        txn_type = request.form.get('type', '').strip()
        category = request.form.get('category', '').strip()

        if not title or not amount_str or not txn_type or not category:
            flash('Please fill in all fields.', 'danger')
            return redirect(url_for('main.edit_transaction', txn_id=txn_id))

        try:
            amount = float(amount_str)
        except ValueError:
            flash('Amount must be a valid number.', 'danger')
            return redirect(url_for('main.edit_transaction', txn_id=txn_id))

        if amount <= 0:
            flash('Amount must be greater than zero.', 'danger')
            return redirect(url_for('main.edit_transaction', txn_id=txn_id))

        if txn_type not in ['income', 'expense']:
            flash('Transaction type must be "income" or "expense".', 'danger')
            return redirect(url_for('main.edit_transaction', txn_id=txn_id))

        txn.title = title
        txn.amount = amount
        txn.type = txn_type
        txn.category = category

        db.session.commit()
        flash('Transaction updated successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_transaction.html', txn=txn)


@main.route('/delete/<int:txn_id>', methods=['POST'])
@login_required
def delete_transaction(txn_id):
    txn = Transaction.query.get_or_404(txn_id)

    if txn.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.dashboard'))

    db.session.delete(txn)
    db.session.commit()
    flash('Transaction deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/support', methods=['GET', 'POST'])
@login_required
def support():
    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        message_body = request.form.get('message', '').strip()

        if not subject or not message_body:
            flash('Please provide both subject and message.', 'danger')
            return render_template('support.html')

        flash('Your message has been sent to support! We will get back to you soon.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('support.html')
