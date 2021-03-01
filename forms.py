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

class EditPasswordForm(FlaskForm):
    password = PasswordField(
        "Current Password",
        validators=[InputRequired(), Length(min=6, max=35), EqualTo('confirm', message='Passwords must match')],
    )
    confirm = PasswordField(
        'Confirm Current Password',
    )
    new_password = PasswordField(
        "New Password",
        validators=[InputRequired(), Length(min=6, max=35), EqualTo('confirm_new_password', message='New passwords must match')],
    )
    confirm_new_password = PasswordField(
        'Confirm New Password',
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
    start_date = DateField(
        "When will the lesson start?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )
    end_date = DateField(
        "When will the lesson end?", format='%Y-%m-%d',
    )
    resources = SelectField(
        "Add Primary Resource", coerce=int
    )

class EditLessonForm(FlaskForm):
    """Edit lesson plan, for logged in user"""
    title = StringField(
        "Lesson Name/Title",
        validators=[InputRequired(), Length(min=1, max=75)],
    )
    summary = TextAreaField(
        "Summary",
    )
    start_date = DateField(
        "When will the lesson start?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )
    end_date = DateField(
        "When will the lesson end?", format='%Y-%m-%d',
    )
    resources = SelectField(
        "Add Primary Resource", coerce=int
    )

class EditResourceForm(FlaskForm):
    """Edit Resource from LOC API, inclduing adding more easy-to-read info (nickname)"""    
    title = StringField(
        "Resource Name/Title",
        validators=[InputRequired(), Length(min=1, max=75)],
    )
    description = TextAreaField(
        "Description (Optional)",
    )
    lesson = SelectField(
        "Add to a Lesson Plan", coerce=int
    )
