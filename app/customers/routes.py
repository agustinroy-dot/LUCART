from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.customers import customers_bp
from app.customers.forms import CustomerForm
from app.models import Customer, Order, Quote

@customers_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    customers = Customer.query.order_by(Customer.name.asc()).paginate(page=page, per_page=20, error_out=False)
    return render_template('customers/index.html', title='Customers', customers=customers)

@customers_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            notes=form.notes.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer created successfully.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('customers/edit.html', title='New Customer', form=form)

@customers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    form = CustomerForm(obj=customer)
    if form.validate_on_submit():
        customer.name = form.name.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        customer.address = form.address.data
        customer.notes = form.notes.data
        db.session.commit()
        flash('Customer updated successfully.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('customers/edit.html', title='Edit Customer', form=form, customer=customer)

@customers_bp.route('/<int:id>')
@login_required
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    # Get history
    orders = customer.orders.order_by(Order.date_created.desc()).all()
    quotes = customer.quotes.order_by(Quote.date.desc()).all()
    return render_template('customers/view.html', customer=customer, orders=orders, quotes=quotes)
