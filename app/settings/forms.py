from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class SettingsForm(FlaskForm):
    electricity_rate = FloatField('Electricity Rate ($/kWh)', validators=[DataRequired()])
    labor_rate = FloatField('Labor Rate ($/h)', validators=[DataRequired()])
    default_margin = FloatField('Default Margin (0.30 = 30%)', validators=[DataRequired()])
    consumables_cost = FloatField('Default Consumables Cost ($)', validators=[DataRequired()])
    logo = FileField('Upload Logo (PNG/JPG)', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Save Settings')
