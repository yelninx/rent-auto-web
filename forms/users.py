from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('rember')
    submit = SubmitField('Sign in')

class EditUserForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    is_admin = StringField('Is Admin', validators=[DataRequired()])
    submit = SubmitField('Confirm')


class RegisterForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password_again = PasswordField('repeat password', validators=[DataRequired()])

    submit = SubmitField('Sign up')