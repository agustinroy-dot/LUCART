from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional

class QuoteForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notes/Conditions')
    submit = SubmitField('Save Quote')

class QuoteItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=1, validators=[DataRequired()])
    unit_price = FloatField('Unit Price', default=0.0, validators=[DataRequired()])
    submit = SubmitField('Add Item')

class CalculatorForm(FlaskForm):
    machine_id = SelectField('Machine', coerce=int, validators=[DataRequired()])
    material_id = SelectField('Material', coerce=int, validators=[DataRequired()])
    weight_g = FloatField('Weight (g)', validators=[DataRequired()])
    print_time_h = FloatField('Print Time (hours)', validators=[DataRequired()])
    labor_time_h = FloatField('Labor Time (hours)', default=0.25, validators=[DataRequired()])
    margin = FloatField('Margin (0.30 = 30%)', default=0.30, validators=[DataRequired()])
    description = StringField('Item Description', validators=[DataRequired()])
    submit = SubmitField('Calculate & Add Item')
