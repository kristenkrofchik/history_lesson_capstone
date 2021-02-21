from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
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
        validators=[InputRequired(), Length(min=6, max=35)],
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
        "When will thie Lesson begin?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )
    end_date = DateField(
        "When will this lesson be completed?", format='%Y-%m-%d',
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
    start_date = DateField(
        "When will thie Lesson begin?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )
    end_date = DateField(
        "When will this lesson be completed?", format='%Y-%m-%d',
        validators=[InputRequired()],
    )


#class UserSearchForm(FlaskForm):
#    """Search users by username, last_name, location, grade, school"""
#    choices = [('Username', 'Username'),
#                ('Last Name')]
