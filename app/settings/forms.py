from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Optional

class SettingsForm(FlaskForm):
    business_name = StringField('Business Name', validators=[Optional()])
    address = StringField('Address', validators=[Optional()])
    cuit = StringField('CUIT/Tax ID', validators=[Optional()])
    submit = SubmitField('Save Settings')
