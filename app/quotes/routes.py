from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.quotes import quotes_bp
from app.quotes.forms import QuoteForm, QuoteItemForm, CalculatorForm
from app.models import Quote, QuoteItem, Customer, Order, OrderItem, Machine, Material, AppSetting
from datetime import datetime
from sqlalchemy.orm import joinedload

@quotes_bp.route('/')
@login_required
def index():
    # Optimizing: Eager load Customer to prevent N+1 queries
    quotes = Quote.query.options(joinedload(Quote.customer)).order_by(Quote.date.desc()).all()
    return render_template('quotes/index.html', title='Quotes', quotes=quotes)

@quotes_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_quote():
    form = QuoteForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by('name').all()]

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
        quote.total += (item.quantity * item.unit_price)
        db.session.commit()
        return redirect(url_for('quotes.view_quote', id=quote.id))

    return render_template('quotes/view.html', quote=quote, item_form=item_form)

@quotes_bp.route('/<int:id>/calculator', methods=['GET', 'POST'])
@login_required
def calculator(id):
    quote = Quote.query.get_or_404(id)
    form = CalculatorForm()

    # Populate choices
    form.machine_id.choices = [(m.id, m.name) for m in Machine.query.all()]
    form.material_id.choices = [(m.id, f"{m.name} ({m.cost}/{m.unit})") for m in Material.query.all()]

    # Set defaults from settings
    if request.method == 'GET':
        form.margin.data = float(AppSetting.get('default_margin', 0.30))

    if form.validate_on_submit():
        machine = Machine.query.get(form.machine_id.data)
        material = Material.query.get(form.material_id.data)

        weight_g = form.weight_g.data
        time_h = form.print_time_h.data
        labor_h = form.labor_time_h.data
        margin = form.margin.data

        # Get Rates
        elec_rate = float(AppSetting.get('electricity_rate', 0.25))
        labor_rate = float(AppSetting.get('labor_rate', 20.0))
        consumables = float(AppSetting.get('consumables_cost', 2.0))

        # 1. Material Cost
        cost_per_g = material.cost
        if material.unit.lower() in ['kg', 'kilogram']:
            cost_per_g = material.cost / 1000.0
        elif material.unit.lower() in ['l', 'liter']:
             if material.unit.lower() == 'l':
                 cost_per_g = material.cost / 1000.0

        mat_cost = weight_g * cost_per_g

        # 2. Energy
        energy_cost = time_h * (machine.power_consumption_watts / 1000.0) * elec_rate

        # 3. Machine Wear
        machine_cost = time_h * machine.hourly_cost

        # 4. Labor
        labor_cost = labor_h * labor_rate

        # Total Base
        base_cost = mat_cost + energy_cost + machine_cost + labor_cost + consumables

        # Final Price
        final_price = base_cost * (1 + margin)

        # Create Item
        desc = f"{form.description.data} (Mat: {weight_g}g {material.name}, Time: {time_h}h on {machine.name})"

        item = QuoteItem(
            quote_id=quote.id,
            description=desc,
            quantity=1,
            unit_price=round(final_price, 2)
        )
        db.session.add(item)
        quote.total += item.unit_price
        db.session.commit()

        flash(f'Calculated Item Added! Price: ${round(final_price, 2)} (Cost: ${round(base_cost, 2)})', 'success')
        return redirect(url_for('quotes.view_quote', id=quote.id))

    return render_template('quotes/calculator.html', form=form, quote=quote)


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
    db.session.flush()

    # Copy Items
    for qi in quote.items:
        oi = OrderItem(
            order_id=order.id,
            description=qi.description,
            quantity=qi.quantity,
            unit_price=qi.unit_price
        )
        db.session.add(oi)

    db.session.commit()

    flash(f'Order #{order.id} created from Quote #{quote.id}.', 'success')
    return redirect(url_for('orders.view_order', id=order.id))
