from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    username = StringField("username" , validators=[DataRequired()])
    password = PasswordField("password" , validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class EditAccountForm(FlaskForm):
    # id = HiddenField('id', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    nome = StringField('nome', validators=[DataRequired()])
    cpf = StringField('cpf', validators=[DataRequired()])
    pis = StringField('pis', validators=[DataRequired()])
