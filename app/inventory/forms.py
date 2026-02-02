from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class MaterialForm(FlaskForm):
    name = StringField('Material Name', validators=[DataRequired()])
    type = SelectField('Type', choices=[('Filament', 'Filament'), ('Resin', 'Resin'), ('Component', 'Component'), ('Other', 'Other')])
    quantity = FloatField('Current Quantity', default=0.0)
    unit = StringField('Unit (e.g., g, kg, ml)', validators=[DataRequired()])
    cost = FloatField('Unit Cost (avg)', default=0.0)
    min_stock = FloatField('Minimum Stock Alert Level', default=0.0)
    submit = SubmitField('Save Material')

class StockUpdateForm(FlaskForm):
    change_amount = FloatField('Quantity to Add/Remove', validators=[DataRequired()])
    type = SelectField('Action', choices=[('in', 'Add Stock (Purchase/Return)'), ('out', 'Remove Stock (Usage/Waste)')])
    reason = StringField('Reason (e.g., PO #123, Print Job)', validators=[Optional()])

    # Options for Purchase
    cost_total = FloatField('Total Purchase Cost', validators=[Optional()])
    create_expense = BooleanField('Record as Expense in Finances?')

    submit = SubmitField('Update Stock')
