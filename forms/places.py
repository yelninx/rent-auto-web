from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class EditPlaceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    owner_id = IntegerField('Owner', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    submit = SubmitField('Done')
