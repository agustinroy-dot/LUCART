from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class QuoteForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    notes = TextAreaField('Notes/Conditions')
    submit = SubmitField('Save Quote')

class QuoteItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', default=1, validators=[DataRequired()])
    unit_price = FloatField('Unit Price', default=0.0, validators=[DataRequired()])
    submit = SubmitField('Add Item')
