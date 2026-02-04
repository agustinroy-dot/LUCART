from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class MachineForm(FlaskForm):
    name = StringField('Machine Name', validators=[DataRequired()])
    hourly_cost = FloatField('Hourly Cost ($)', validators=[DataRequired()])
    power_consumption_watts = FloatField('Power Consumption (Watts)', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Active', 'Active'), ('Maintenance', 'Maintenance'), ('Retired', 'Retired')])
    submit = SubmitField('Save Machine')
