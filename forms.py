from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],)


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],)


class SearchForm(FlaskForm):
    query = StringField(
        "Search for drink",
        validators=[InputRequired(), Length(min=1, max=20)],)
