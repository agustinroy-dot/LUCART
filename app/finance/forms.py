from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, BooleanField, SubmitField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

class TransactionForm(FlaskForm):
    date = DateField('Date', default=datetime.utcnow, validators=[DataRequired()])
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], default='expense')
    category = StringField('Category (e.g., Material, Sales, Rent)', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    description = StringField('Description')
    is_business = BooleanField('Business Transaction?', default=True)
    submit = SubmitField('Save Transaction')
