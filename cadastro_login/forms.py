from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("username" , validators=[DataRequired()])
    password = PasswordField("password" , validators=[DataRequired()])
    remember_me = BooleanField("remember_me")
