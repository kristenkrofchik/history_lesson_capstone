from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional, EqualTo
from wtforms.fields.html5 import DateField
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=35), EqualTo('confirm', message='Passwords must match')],
    )
    confirm = PasswordField(
        'Repeat Password',
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )


class LoginForm(FlaskForm):
    """User Login Form"""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=35)],
    )

class EditUserForm(FlaskForm):
    """Edit User Profile Form"""
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name (Optional)",
        validators=[Length(max=30)],
    )
    last_name = StringField(
        "Last Name (Optional)",
        validators=[Length(max=30)],
    )
    school = StringField(
        "School Name (Optional)",
        validators=[Length(max=40)]
    )
    grade = StringField(
        "Grade (Optional)",
        validators=[Length(max=15)]
    )
    location = StringField(
        "Location (Optional)",
        validators=[Length(max=30)]
    )

class AddLessonForm(FlaskForm):
    """Add New Lesson Plan, for Logged in User"""
    title = StringField(
        "Lesson Name/Title",
        validators=[InputRequired(), Length(min=1, max=75)],
    )
    summary = TextAreaField(
        "Summary (Optional)",
    )
    date = DateField(
        "When will thie Lesson take place?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )

class EditLessonForm(FlaskForm):
    """Edit lesson plan, for logged in user"""
    title = StringField(
        "Lesson Name/Title",
        validators=[InputRequired(), Length(min=1, max=75)],
    )
    summary = TextAreaField(
        "Summary (Optional)",
    )
    date = DateField(
        "When will thie Lesson take place?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )

#class AddResourceForm(FlaskForm):
    """Add Resource from LOC API search to user profile"""
 #   title = 
