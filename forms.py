from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=35)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name",
        validators=[Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[Length(max=30)],
    )
    school = StringField(
        "School Name",
        validators=[Length(max=40)]
    )
    grade = StringField(
        "Grade",
        validators=[Length(max=15)]
    )
    location = StringField(
        "Location",
        validators=[Length(max=30)]
    )

