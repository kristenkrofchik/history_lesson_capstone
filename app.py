from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from forms import RegisterForm, LoginForm, AddLessonForm
from models import db, connect_db, Follows, User, Lesson, Resource


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///history-lesson"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()



@app.route('/')
def homepage():
    """Homepage. Redirect to Register Page"""
    return redirect('/register')

@app.route('/register', methods=['GET'])
def show_register_form():
    """Show Register Form"""

    if "id" in session:
        return redirect(f"/users/{session['id']}")

    form = RegisterForm()

    return render_template("register.html", form=form)
    
@app.route('/register', methods=['POST'])
def handle_register_form():
    """Handle Register Form"""

    if "id" in session:
        return redirect(f"/users/{session['id']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        school = form.school.data
        grade = form.grade.data
        location = form.location.data

        user = User.signup(username, password, email, first_name, last_name, school, grade, location)

        db.session.commit()
        session['id'] = user.id

        return redirect(f"/users/{user.id}")

    else:
        return render_template("register.html", form=form)

@app.route('/login', methods=['GET'])
def show_login_form():
    """Show Login Form"""

    if "id" in session:
        return redirect(f"/users/{session['id']}")

    form = LoginForm()

    return render_template("login.html", form=form)

@app.route('/login', methods=['POST'])
def handle_login_form():
    """Handle Login Form"""
    if "id" in session:
        return redirect(f"/users/{session['id']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  
        
        if user:
            session['id'] = user.id
            return redirect(f"/users/{user.id}")
        else:
            form.username.errors = ["The username or password you entered is incorrect."]
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)

@app.route("/logout")
def logout_user():
    """Logout user."""

    session.pop("id")
    return redirect("/login")

#@app.route('/users')
#def show_users():
    #"""List all users"""


@app.route(f"/users/<int:user_id>")
def show_user_home(user_id):
    """Show Logged In User Homepage"""
    """Homepage will also need: user calendar,
    search for other users, show user profile info (template), logout, reccomended resoucres?"""
    user = User.query.get_or_404(user_id)

    return render_template('users/home.html', user=user)

@app.route(f"/users/<int:user_id>/lessons")
def show_user_lessons(user_id):
    """Show a list of user lessons (seperate from user home which will show all scheduled lessons on a calendar. this will be a list of lessons). page is only accessible to the logged in user."""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    lessons = (Lesson.query.filter(Lesson.user_id == user_id)
                .order_by(Lesson.timestamp.desc())
                .all())
    
    return render_template('users/lessons.html', user=user, lessons=lessons)

@app.route(f"/users/<int:user_id>/lessons/new", methods=['GET'])
def show_add_lesson_form(user_id):
    """show form for adding a lesson plan"""
    
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    form = AddLessonForm()

    return render_template("lessons/new.html", form=form)


@app.route(f"/users/<int:user_id>/lessons/new", methods=['POST'])
def handle_add_lesson_form(user_id):
    """Submit New Lesson plan and redirect to user home"""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    form = AddLessonForm()

    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        start_date = form.start_date.data
        end_date = form.end_date.data

        lesson = Lesson(
            title=title,
            summary=summary,
            start_date=start_date,
            end_date=end_date
        )

        db.session.add(lesson)
        db.session.commit()

        return redirect(f"/users/{user.id}")

    else:
        return render_template("lessons/new.html", form=form)





