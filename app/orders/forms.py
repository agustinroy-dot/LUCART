from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class OrderForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    price = FloatField('Agreed Price', default=0.0)
    date_due = DateField('Due Date', validators=[Optional()])
    status = SelectField('Status', choices=[
        ('Pending', 'Pending'),
        ('In Production', 'In Production'),
        ('Finished', 'Finished'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    submit = SubmitField('Save Order')

class OrderMaterialForm(FlaskForm):
    material_id = SelectField('Material', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity Used/Est', validators=[DataRequired()])
    submit = SubmitField('Add Material')

class ConfirmMaterialForm(FlaskForm):
    quantity_real = FloatField('Real Quantity Used', validators=[DataRequired()])
    submit = SubmitField('Confirm & Deduct')
