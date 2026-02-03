from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.finance import finance_bp
from app.finance.forms import TransactionForm
from app.models import Transaction
from sqlalchemy import extract, func, case
from datetime import datetime

@finance_bp.route('/')
@login_required
def index():
    # Filters
    month = request.args.get('month', datetime.now().month, type=int)
    year = request.args.get('year', datetime.now().year, type=int)
    scope = request.args.get('scope', 'business') # business, personal, all

    query = Transaction.query.filter(extract('year', Transaction.date) == year, extract('month', Transaction.date) == month)

    if scope == 'business':
        query = query.filter_by(is_business=True)
    elif scope == 'personal':
        query = query.filter_by(is_business=False)

    transactions = query.order_by(Transaction.date.desc()).all()

    # Summary
    # Optimized: Use SQL aggregation instead of Python iteration
    sums = query.with_entities(
        func.sum(case((Transaction.type == 'income', Transaction.amount), else_=0)),
        func.sum(case((Transaction.type == 'expense', Transaction.amount), else_=0))
    ).first()

    income = sums[0] or 0
    expenses = sums[1] or 0
    balance = income - expenses

    return render_template('finance/index.html', title='Finance', transactions=transactions,
                           income=income, expenses=expenses, balance=balance,
                           month=month, year=year, scope=scope)

@finance_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        txn = Transaction(
            date=form.date.data,
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data,
            description=form.description.data,
            is_business=form.is_business.data
        )
        db.session.add(txn)
        db.session.commit()
        flash('Transaction recorded.', 'success')
        return redirect(url_for('finance.index'))
    return render_template('finance/edit.html', title='New Transaction', form=form)

@finance_bp.route('/<int:id>/delete')
@login_required
def delete_transaction(id):
    txn = Transaction.query.get_or_404(id)
    db.session.delete(txn)
    db.session.commit()
    flash('Transaction deleted.', 'success')
    return redirect(url_for('finance.index'))
