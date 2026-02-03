from flask import render_template, flash, redirect, url_for, Response, request
from flask_login import login_required
from app import db
from app.settings import settings_bp
from app.settings.forms import SettingsForm
from app.models import Customer, Order, Transaction, Material, InventoryLog, AppSetting
import csv
import io

@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SettingsForm()
    # Fetch the singleton settings object
    app_setting = db.session.get(AppSetting, 1)

    if form.validate_on_submit():
        if not app_setting:
            app_setting = AppSetting(id=1)
            db.session.add(app_setting)

        app_setting.business_name = form.business_name.data
        app_setting.address = form.address.data
        app_setting.cuit = form.cuit.data

        db.session.commit()
        flash('Settings saved successfully.', 'success')
        return redirect(url_for('settings.index'))

    if request.method == 'GET' and app_setting:
        form.business_name.data = app_setting.business_name
        form.address.data = app_setting.address
        form.cuit.data = app_setting.cuit

    return render_template('settings/index.html', title='Settings & Data', form=form)

@settings_bp.route('/export/<type>')
@login_required
def export_data(type):
    si = io.StringIO()
    cw = csv.writer(si)

    if type == 'customers':
        cw.writerow(['ID', 'Name', 'Email', 'Phone', 'Address', 'Notes'])
        records = Customer.query.all()
        for r in records:
            cw.writerow([r.id, r.name, r.email, r.phone, r.address, r.notes])
        filename = 'customers.csv'

    elif type == 'orders':
        cw.writerow(['ID', 'Customer', 'Description', 'Price', 'Status', 'Date Created', 'Date Due'])
        records = Order.query.all()
        for r in records:
            cw.writerow([r.id, r.customer.name if r.customer else 'N/A', r.description, r.price, r.status, r.date_created, r.date_due])
        filename = 'orders.csv'

    elif type == 'finance':
        cw.writerow(['ID', 'Date', 'Type', 'Category', 'Amount', 'Description', 'Is Business'])
        records = Transaction.query.all()
        for r in records:
            cw.writerow([r.id, r.date, r.type, r.category, r.amount, r.description, r.is_business])
        filename = 'transactions.csv'

    elif type == 'inventory':
        cw.writerow(['ID', 'Name', 'Type', 'Quantity', 'Unit', 'Cost'])
        records = Material.query.all()
        for r in records:
            cw.writerow([r.id, r.name, r.type, r.quantity, r.unit, r.cost])
        filename = 'inventory.csv'

    else:
        flash('Invalid export type.', 'error')
        return redirect(url_for('settings.index'))

    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-disposition":
                 f"attachment; filename={filename}"}
    )
