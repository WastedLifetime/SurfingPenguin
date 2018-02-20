"""forms.py: This file contains classes that respectively represent a form."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ShortAnswerForm(FlaskForm):
    content = StringField('Answer', validators=[DataRequired()])

class SubmitForm(FlaskForm):
    submit = SubmitField('Answer', validators=[DataRequired()])

