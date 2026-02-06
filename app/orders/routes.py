from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.orders import orders_bp
from app.orders.forms import OrderForm, OrderMaterialForm, ConfirmMaterialForm
from app.models import Order, OrderMaterial, Customer, Material, InventoryLog, Transaction
from datetime import datetime
from sqlalchemy.orm import joinedload

@orders_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status')
    query = Order.query.options(joinedload(Order.customer))
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.date_created.desc()).all()
    return render_template('orders/index.html', title='Orders', orders=orders)

@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by('name').all()]

    if form.validate_on_submit():
        order = Order(
            customer_id=form.customer_id.data,
            description=form.description.data,
            price=form.price.data,
            date_due=form.date_due.data,
            status=form.status.data,
            date_created=datetime.utcnow()
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('orders.view_order', id=order.id))
    return render_template('orders/edit.html', title='New Order', form=form)

@orders_bp.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def view_order(id):
    order = Order.query.options(joinedload(Order.materials).joinedload(OrderMaterial.material)).get_or_404(id)
    mat_form = OrderMaterialForm()
    mat_form.material_id.choices = [(m.id, f"{m.name} ({m.unit})") for m in Material.query.order_by('name').all()]

    if mat_form.validate_on_submit():
        # Check if already added?
        existing = OrderMaterial.query.filter_by(order_id=order.id, material_id=mat_form.material_id.data).first()
        if existing:
            mat_form.material_id.errors.append("Este material ya ha sido agregado al pedido.")
        else:
            om = OrderMaterial(
                order_id=order.id,
                material_id=mat_form.material_id.data,
                quantity_estimated=mat_form.quantity.data,
                quantity_real=0.0 # Confirmed later
            )
            db.session.add(om)
            db.session.commit()
            flash('Material usage estimate added.', 'success')
            return redirect(url_for('orders.view_order', id=order.id))

    return render_template('orders/view.html', order=order, mat_form=mat_form)

@orders_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=order)
    form.customer_id.choices = [(c.id, c.name) for c in Customer.query.order_by('name').all()]

    if form.validate_on_submit():
        order.customer_id = form.customer_id.data
        order.description = form.description.data
        order.price = form.price.data
        order.date_due = form.date_due.data
        order.status = form.status.data
        db.session.commit()
        flash('Order updated.', 'success')
        return redirect(url_for('orders.view_order', id=order.id))
    return render_template('orders/edit.html', title='Edit Order', form=form)

@orders_bp.route('/material/<int:id>/deduct', methods=['GET', 'POST'])
@login_required
def confirm_material_usage(id):
    # This ID is the OrderMaterial ID
    om = OrderMaterial.query.get_or_404(id)

    # Idempotency Check: if already deducted (quantity_real > 0), don't deduct again
    if om.quantity_real > 0:
        flash('Material already deducted for this item.', 'warning')
        return redirect(url_for('orders.view_order', id=om.order_id))

    form = ConfirmMaterialForm()

    if form.validate_on_submit():
        real_qty = form.quantity_real.data
        material = om.material

        if material.quantity < real_qty:
             flash(f'Not enough stock of {material.name} (Available: {material.quantity} {material.unit}) for usage of {real_qty} {material.unit}!', 'error')
             return render_template('orders/confirm_material.html', om=om, form=form)

        # Deduct
        material.quantity -= real_qty
        om.quantity_real = real_qty

        # Log
        log = InventoryLog(
            material_id=material.id,
            change_amount=real_qty,
            type='out',
            reason=f"Order #{om.order_id}",
            date=datetime.utcnow()
        )
        db.session.add(log)
        db.session.commit()
        flash(f'Stock deducted successfully ({real_qty} {material.unit}).', 'success')
        return redirect(url_for('orders.view_order', id=om.order_id))

    # Pre-fill
    if request.method == 'GET':
        form.quantity_real.data = om.quantity_estimated

    return render_template('orders/confirm_material.html', om=om, form=form)

@orders_bp.route('/<int:id>/pay')
@login_required
def mark_paid(id):
    order = Order.query.get_or_404(id)

    # Idempotency Check
    if order.payment_status == 'Paid':
        flash('Order already paid.', 'info')
        return redirect(url_for('orders.view_order', id=id))

    # Also check if a transaction for this order already exists to be extra safe
    existing_txn = Transaction.query.filter_by(description=f"Order #{order.id} - {order.customer.name}").first()
    if existing_txn:
         flash('Transaction for this order already recorded.', 'warning')
         order.payment_status = 'Paid' # Ensure consistency
         db.session.commit()
         return redirect(url_for('orders.view_order', id=id))

    order.payment_status = 'Paid'

    # Create Income
    txn = Transaction(
        date=datetime.utcnow(),
        type='income',
        category='Sales',
        amount=order.price,
        description=f"Order #{order.id} - {order.customer.name}",
        is_business=True
    )
    db.session.add(txn)
    db.session.commit()
    flash('Order marked as Paid and Income recorded.', 'success')
    return redirect(url_for('orders.view_order', id=id))
