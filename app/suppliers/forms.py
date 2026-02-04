from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class SupplierForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_info = StringField('Contact Info')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Supplier')
