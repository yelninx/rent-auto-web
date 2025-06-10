from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired


class EditCarForm(FlaskForm):
    model = StringField('Model', validators=[DataRequired()])
    brand = StringField('Brand', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    is_taken = StringField('Is Taken', validators=[DataRequired()])
    place_id = IntegerField('Place', validators=[DataRequired()])
    image = FileField('File', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Выберите изображение')])
    submit = SubmitField('Done')
