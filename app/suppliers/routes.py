from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.suppliers import suppliers_bp
from app.suppliers.forms import SupplierForm
from app.models import Supplier

@suppliers_bp.route('/')
@login_required
def index():
    suppliers = Supplier.query.all()
    return render_template('suppliers/index.html', title='Suppliers', suppliers=suppliers)

@suppliers_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_info=form.contact_info.data,
            notes=form.notes.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier added successfully.', 'success')
        return redirect(url_for('suppliers.index'))
    return render_template('suppliers/edit.html', title='New Supplier', form=form)

@suppliers_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_info = form.contact_info.data
        supplier.notes = form.notes.data
        db.session.commit()
        flash('Supplier updated successfully.', 'success')
        return redirect(url_for('suppliers.index'))
    return render_template('suppliers/edit.html', title='Edit Supplier', form=form)

@suppliers_bp.route('/<int:id>/delete')
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier deleted.', 'success')
    return redirect(url_for('suppliers.index'))
