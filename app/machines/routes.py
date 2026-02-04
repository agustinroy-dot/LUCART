from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
from app import db
from app.machines import machines_bp
from app.machines.forms import MachineForm
from app.models import Machine

@machines_bp.route('/')
@login_required
def index():
    machines = Machine.query.all()
    return render_template('machines/index.html', title='Machines', machines=machines)

@machines_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_machine():
    form = MachineForm()
    if form.validate_on_submit():
        machine = Machine(
            name=form.name.data,
            hourly_cost=form.hourly_cost.data,
            power_consumption_watts=form.power_consumption_watts.data,
            status=form.status.data
        )
        db.session.add(machine)
        db.session.commit()
        flash('Machine added successfully.', 'success')
        return redirect(url_for('machines.index'))
    return render_template('machines/edit.html', title='New Machine', form=form)

@machines_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_machine(id):
    machine = Machine.query.get_or_404(id)
    form = MachineForm(obj=machine)
    if form.validate_on_submit():
        machine.name = form.name.data
        machine.hourly_cost = form.hourly_cost.data
        machine.power_consumption_watts = form.power_consumption_watts.data
        machine.status = form.status.data
        db.session.commit()
        flash('Machine updated successfully.', 'success')
        return redirect(url_for('machines.index'))
    return render_template('machines/edit.html', title='Edit Machine', form=form)

@machines_bp.route('/<int:id>/delete')
@login_required
def delete_machine(id):
    machine = Machine.query.get_or_404(id)
    db.session.delete(machine)
    db.session.commit()
    flash('Machine deleted.', 'success')
    return redirect(url_for('machines.index'))
