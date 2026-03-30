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
    if type not in ['customers', 'orders', 'finance', 'inventory']:
        flash('Invalid export type.', 'error')
        return redirect(url_for('settings.index'))

    def generate():
        si = io.StringIO()
        cw = csv.writer(si)

        if type == 'customers':
            cw.writerow(['ID', 'Name', 'Email', 'Phone', 'Address', 'Notes'])
            yield si.getvalue()
            si.seek(0); si.truncate(0)

            for r in Customer.query.yield_per(100):
                cw.writerow([r.id, r.name, r.email, r.phone, r.address, r.notes])
                yield si.getvalue()
                si.seek(0); si.truncate(0)

        elif type == 'orders':
            cw.writerow(['ID', 'Customer', 'Description', 'Price', 'Status', 'Date Created', 'Date Due'])
            yield si.getvalue()
            si.seek(0); si.truncate(0)

            # Use joinedload for the many-to-one customer relationship to avoid N+1 queries during export
            for r in Order.query.options(joinedload(Order.customer)).yield_per(100):
                cw.writerow([r.id, r.customer.name if r.customer else 'N/A', r.description, r.price, r.status, r.date_created, r.date_due])
                yield si.getvalue()
                si.seek(0); si.truncate(0)

        elif type == 'finance':
            cw.writerow(['ID', 'Date', 'Type', 'Category', 'Amount', 'Description', 'Is Business'])
            yield si.getvalue()
            si.seek(0); si.truncate(0)

            for r in Transaction.query.yield_per(100):
                cw.writerow([r.id, r.date, r.type, r.category, r.amount, r.description, r.is_business])
                yield si.getvalue()
                si.seek(0); si.truncate(0)

        elif type == 'inventory':
            cw.writerow(['ID', 'Name', 'Type', 'Quantity', 'Unit', 'Cost'])
            yield si.getvalue()
            si.seek(0); si.truncate(0)

            for r in Material.query.yield_per(100):
                cw.writerow([r.id, r.name, r.type, r.quantity, r.unit, r.cost])
                yield si.getvalue()
                si.seek(0); si.truncate(0)

    filename = f"{type}.csv"
    if type == 'finance':
        filename = 'transactions.csv'

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )
