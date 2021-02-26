from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from forms import RegisterForm, LoginForm, AddLessonForm, EditLessonForm, EditUserForm
from models import db, connect_db, Follows, User, Lesson, Resource, serialize_user, serialize_lesson, serialize_resource


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///history-lesson"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

"""Register, Login, Logout Routes"""

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

        user = User.signup(username, password, email)

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

"""Users/User Routes"""

@app.route('/users')
def show_users():
    """Browse all users, search users"""
    """Have to add authentication so if not that user you can see profile but not edit it"""
    """add search function for users"""

    user_id = session['id']
    user = User.query.get_or_404(user_id)

    users = User.query.all()

    return render_template('users/all.html', user=user, users=users)


@app.route(f"/users/<int:user_id>", methods=['GET', 'POST'])
def show_user_home(user_id):
    """Show Logged In User Homepage"""
    """Homepage will also need: user calendar,
    search for other users, show user profile info (template), logout, reccomended resoucres?"""
    user = User.query.get_or_404(user_id)

    return render_template('users/home.html', user=user)

@app.route(f"/users/<int:user_id>/edit", methods=['GET'])
def show_edit_user_form(user_id):
    """Show form to edit user profile info"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    form = EditUserForm(obj=user)

    return render_template("users/edit.html", user=user, form=form)


@app.route(f"/users/<int:user_id>/edit", methods=['POST'])
def handle_edit_user_form(user_id):
    """Handle form to edit user profile info, redirect to user home"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.school = form.school.data
        user.grade = form.grade.data
        user.location = form.location.data

        db.session.commit()

        return redirect(f"/users/{user.id}")

    return render_template("users/edit.html", form=form, user=user)


@app.route(f"/users/<int:user_id>/lessons")
def show_user_lessons(user_id):
    """Show a list of user lessons (seperate from user home which will show all scheduled lessons on a calendar. this will be a list of lessons). page is only accessible to the logged in user."""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    lessons = (Lesson.query.filter(Lesson.user_id == user_id)
                .all())
    
    return render_template('users/lessons.html', user=user, lessons=lessons)

"""Lesson Routes"""

@app.route('/lessons/new')
def show_add_lesson_form_from_cal():
    """show form for adding a lesson plan from js calendar link"""
    user = User.query.get_or_404(session['id'])

    if "id" not in session or user.id != session['id']:
        raise Unauthorized()

    form = AddLessonForm()

    return render_template("lessons/new.html", form=form)


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
        start_date = form.start_date.data.strftime('%Y-%m-%d')
        end_date = form.end_date.data.strftime('%Y-%m-%d')


        lesson = Lesson(
            title=title,
            summary=summary,
            start_date=start_date,
            end_date=end_date,
            user_id=user.id
        )

        db.session.add(lesson)
        db.session.commit()

        return redirect(f"/users/{user.id}")

    else:
        return render_template("lessons/new.html", form=form)

@app.route(f"/lessons/<int:lesson_id>")
def show_single_lesson(lesson_id):
    """Show information about a single lesson"""
    lesson = Lesson.query.get(lesson_id)
    user = lesson.user

    return render_template('/lessons/detail.html', lesson=lesson, user=user)


@app.route(f"/lessons/<int:lesson_id>/edit", methods=['GET'])
def show_edit_lesson_form(lesson_id):
    """Show form to edit a lesson plan"""
    lesson = Lesson.query.get(lesson_id)

    if "id" not in session or lesson.user.id != session['id']:
        raise Unauthorized()

    form = EditLessonForm(obj=lesson)

    return render_template('/lessons/edit.html', lesson=lesson, form=form)


@app.route(f"/lessons/<int:lesson_id>/edit", methods=['POST'])
def handle_edit_lesson_form(lesson_id):
    """Handle submit of form to edit a lesson plan, redirect to the main page for the lesson"""
    lesson = Lesson.query.get(lesson_id)

    if "id" not in session or lesson.user.id != session['id']:
        raise Unauthorized()

    form = EditLessonForm(obj=lesson)

    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.summary = form.summary.data
        lesson.start_date = form.start_date.data.strftime('%Y-%m-%d')
        lesson.end_date = form.end_date.data.strftime('%Y-%m-%d')

        db.session.commit()

        return redirect(f"/lessons/{lesson.id}")

    return render_template("lessons/edit.html", form=form, lesson=lesson)

@app.route("/lessons/<int:lesson_id>/delete", methods=["POST"])
def delete_lesson(lesson_id):
    """Delete individual lesson."""

    lesson = Lesson.query.get(lesson_id)
    user = lesson.user
    
    if "id" not in session or lesson.user_id != session['id']:
        raise Unauthorized()

    db.session.delete(lesson)
    db.session.commit()

    return redirect(f"/users/{user.id}/lessons")

"""Resource routes"""

@app.route("/resources/search", methods=['GET'])
def show_resource_search_page():
    """show resource search form, where js code will show search results from 3rd party API"""
    user = User.query.get_or_404(session['id'])

    return render_template("resources/search.html", user=user)

#@app.route(f"/users/<int:user_id>/resources/new", methods=['POST'])
#def add_resource():
#    """Select resource from LOC API and add to database & user's profile"""


"""API ROUTES"""

#@app.route("/api/users/<int:user_id>")
#def jsonify_user_data(user_id):

#    user = User.query.get(user_id)
#    serialized = serialize_user(user)

#    return jsonify(user=serialized)

#@app.route("/api/lessons/<int:lesson_id>")
#def jsonify_lesson_data(lesson_id):
#    lesson = Lesson.query.get(lesson_id)
#    serialized = serialize_lesson(lesson)

#    return jsonify(lesson=serialized)


@app.route("/api/resources/add", methods=['GET', 'POST'])
def add_resource():
    user = User.query.get_or_404(session['id'])

    id = request.json["id"]
    title = request.json["title"]
    description = request.json["description"]
    url = request.json["url"]

    new_resource = Resource(id=id, title=title, description=description, url=url)
    
    db.session.add(new_resource)
    db.session.commit()

    return redirect(f"/users/{user.id}", user=user)









