from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, SelectField
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
    start_date = DateTimeField(
        "When will thie Lesson begin?",
        validators=[InputRequired()],
    )
    end_date = DateTimeField(
        "When will this lesson be completed?",
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
    start_date = DateTimeField(
        "When will thie Lesson begin?",
        validators=[InputRequired()],
    )
    end_date = DateTimeField(
        "When will this lesson be completed?",
        validators=[InputRequired()],
    )


#class UserSearchForm(FlaskForm):
#    """Search users by username, last_name, location, grade, school"""
#    choices = [('Username', 'Username'),
#                ('Last Name')]
