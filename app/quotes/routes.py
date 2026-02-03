from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from sqlalchemy.orm import joinedload
from app import db
from app.quotes import quotes_bp
from app.quotes.forms import QuoteForm, QuoteItemForm
from app.models import Quote, QuoteItem, Customer, Order
from datetime import datetime

@quotes_bp.route('/')
@login_required
def index():
    # Optimization: Eager load Customer
    quotes = Quote.query.options(joinedload(Quote.customer)).order_by(Quote.date.desc()).all()
    return render_template('quotes/index.html', title='Quotes', quotes=quotes)

@quotes_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_quote():
    form = QuoteForm()
    # Populate customers
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by('name').all()]

    # Pre-select if customer_id passed in args
    cid = request.args.get('customer_id')
    if cid:
        form.customer_id.data = int(cid)

    if form.validate_on_submit():
        quote = Quote(
            customer_id=form.customer_id.data,
            notes=form.notes.data,
            date=datetime.utcnow()
        )
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('quotes.view_quote', id=quote.id))
    return render_template('quotes/edit.html', title='New Quote', form=form)

@quotes_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def view_quote(id):
    quote = Quote.query.get_or_404(id)
    item_form = QuoteItemForm()

    if item_form.validate_on_submit():
        item = QuoteItem(
            quote_id=quote.id,
            description=item_form.description.data,
            quantity=item_form.quantity.data,
            unit_price=item_form.unit_price.data
        )
        db.session.add(item)
        # Update total
        quote.total += (item.quantity * item.unit_price)
        db.session.commit()
        return redirect(url_for('quotes.view_quote', id=quote.id))

    return render_template('quotes/view.html', quote=quote, item_form=item_form)

@quotes_bp.route('/item/<int:id>/delete')
@login_required
def delete_item(id):
    item = QuoteItem.query.get_or_404(id)
    quote = item.quote
    quote.total -= (item.quantity * item.unit_price)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('quotes.view_quote', id=quote.id))

@quotes_bp.route('/<int:id>/status/<status>')
@login_required
def set_status(id, status):
    quote = Quote.query.get_or_404(id)
    if status in ['Sent', 'Accepted', 'Rejected']:
        quote.status = status
        db.session.commit()
    return redirect(url_for('quotes.view_quote', id=id))

@quotes_bp.route('/<int:id>/print')
@login_required
def print_quote(id):
    quote = Quote.query.get_or_404(id)
    return render_template('quotes/print.html', quote=quote)

@quotes_bp.route('/<int:id>/convert')
@login_required
def convert_to_order(id):
    quote = Quote.query.get_or_404(id)
    if quote.status != 'Accepted':
        flash('Quote must be marked as Accepted before converting.', 'warning')
        return redirect(url_for('quotes.view_quote', id=id))

    # Summarize items
    desc_list = [f"{i.description} (x{i.quantity})" for i in quote.items]
    full_desc = ", ".join(desc_list)

    order = Order(
        customer_id=quote.customer_id,
        description=full_desc,
        price=quote.total,
        status='Pending',
        date_created=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()

    flash(f'Order #{order.id} created from Quote #{quote.id}.', 'success')
    return redirect(url_for('orders.view_order', id=order.id)) # orders.view_order doesn't exist yet
