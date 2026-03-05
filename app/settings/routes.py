from flask import render_template, flash, redirect, url_for, Response, request, current_app
from flask_login import login_required
from app import db
from app.settings import settings_bp
from app.settings.forms import SettingsForm
from app.models import Customer, Order, Transaction, Material, InventoryLog, AppSetting
from sqlalchemy.orm import joinedload
import csv
import io
import os
from werkzeug.utils import secure_filename

@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SettingsForm()

    if form.validate_on_submit():
        AppSetting.set('electricity_rate', form.electricity_rate.data)
        AppSetting.set('labor_rate', form.labor_rate.data)
        AppSetting.set('default_margin', form.default_margin.data)
        AppSetting.set('consumables_cost', form.consumables_cost.data)

        if form.logo.data:
            file = form.logo.data
            filename = 'logo.png' # Force rename to keep it simple for templates
            file.save(os.path.join(current_app.root_path, 'static/img', filename))
            flash('Logo updated successfully!', 'success')

        flash('Settings updated successfully.', 'success')
        return redirect(url_for('settings.index'))

    # Pre-populate form
    if request.method == 'GET':
        form.electricity_rate.data = float(AppSetting.get('electricity_rate', 0.25))
        form.labor_rate.data = float(AppSetting.get('labor_rate', 20.0))
        form.default_margin.data = float(AppSetting.get('default_margin', 0.30))
        form.consumables_cost.data = float(AppSetting.get('consumables_cost', 2.0))

    return render_template('settings/index.html', title='Settings & Data', form=form)

@settings_bp.route('/export/<type>')
@login_required
def export_data(type):
    def generate():
        si = io.StringIO()
        cw = csv.writer(si)

        def write_and_yield(row):
            cw.writerow(row)
            val = si.getvalue()
            si.seek(0)
            si.truncate(0)
            return val

        if type == 'customers':
            yield write_and_yield(['ID', 'Name', 'Email', 'Phone', 'Address', 'Notes'])
            for r in db.session.query(Customer).yield_per(100):
                yield write_and_yield([r.id, r.name, r.email, r.phone, r.address, r.notes])

        elif type == 'orders':
            yield write_and_yield(['ID', 'Customer', 'Description', 'Price', 'Status', 'Date Created', 'Date Due'])
            # .yield_per() is compatible with many-to-one joinedload (like Order->Customer)
            for r in db.session.query(Order).options(joinedload(Order.customer)).yield_per(100):
                yield write_and_yield([r.id, r.customer.name if r.customer else 'N/A', r.description, r.price, r.status, r.date_created, r.date_due])

        elif type == 'finance':
            yield write_and_yield(['ID', 'Date', 'Type', 'Category', 'Amount', 'Description', 'Is Business'])
            for r in db.session.query(Transaction).yield_per(100):
                yield write_and_yield([r.id, r.date, r.type, r.category, r.amount, r.description, r.is_business])

        elif type == 'inventory':
            yield write_and_yield(['ID', 'Name', 'Type', 'Quantity', 'Unit', 'Cost'])
            for r in db.session.query(Material).yield_per(100):
                yield write_and_yield([r.id, r.name, r.type, r.quantity, r.unit, r.cost])

    if type == 'customers':
        filename = 'customers.csv'
    elif type == 'orders':
        filename = 'orders.csv'
    elif type == 'finance':
        filename = 'transactions.csv'
    elif type == 'inventory':
        filename = 'inventory.csv'
    else:
        flash('Invalid export type.', 'error')
        return redirect(url_for('settings.index'))

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )
