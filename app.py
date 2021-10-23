import os

from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import asc
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

#use the package below when testing app with insomnia.
#from flask_wtf.csrf import CSRFProtect

from forms import RegisterForm, LoginForm, AddLessonForm, EditLessonForm, EditUserForm, EditResourceForm, EditPasswordForm
from models import db, connect_db, Follows, User, Lesson, Resource, serialize_resource


app = Flask(__name__)
CORS(app)

#use the package below when testing app with insomnia
#csrf = CSRFProtect(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "postgres:///history-lesson")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nevertell')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()



"""Register, Login, Logout Routes"""



@app.route('/', methods=['GET'])
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
        try:
            username = form.username.data
            password = form.password.data
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            user = User.signup(username, password, email, first_name, last_name)

            db.session.commit()
            session['id'] = user.id

        except IntegrityError as e:
            flash("Username already taken, please enter a different username", 'danger')
            return render_template('register.html', form=form)


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
    """Browse all users"""
    """Have to add authentication so if not that user you can see profile but not edit it"""

    if 'id' in session:
        user_id = session['id']
        user = User.query.get_or_404(user_id)

        users = User.query.all()
        return render_template('users/all.html', user=user, users=users)
        
    else:
        flash('Please login to view.')
        return redirect('/login')

@app.route(f"/users/<int:user_id>", methods=['GET', 'POST'])
def show_user_home(user_id):
    """Show Logged In User Homepage"""
    if 'id' in session:
        user = User.query.get_or_404(user_id)
    
    else:
        flash('Please login to view.')
        return redirect('/login')

    return render_template('users/profile.html', user=user)

@app.route(f"/users/<int:user_id>/profile")
def show_user_profile(user_id):
    """Show logged in user profile page- full profile info, edit profile, following, follower, etc"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    return render_template('users/profile.html', user=user)

@app.route(f"/users/<int:user_id>/calendar")
def show_user_calendar(user_id):
    """Show logged in user calendar page"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    return render_template('users/calendar.html', user=user)


@app.route(f"/users/<int:user_id>/edit", methods=['GET'])
def show_edit_user_form(user_id):
    """Show form to edit user profile info"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditUserForm(obj=user)

    return render_template("users/edit.html", user=user, form=form)


@app.route(f"/users/<int:user_id>/edit", methods=['POST'])
def handle_edit_user_form(user_id):
    """Handle form to edit user profile info, redirect to user home"""
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

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

        return redirect(f"/users/{user.id}/profile")

    return render_template("users/edit.html", form=form, user=user)

@app.route(f"/users/<int:user_id>/edit_password", methods=['GET', 'POST'])
def edit_user_password(user_id):
    """Show & Handle Form to change user password"""
    if "id" not in session or user_id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditPasswordForm()
    user = User.query.get_or_404(user_id)
    username = user.username

    if request.method == 'POST':
        if form.validate_on_submit():
            username = username
            password = form.new_password.data

            user = User.authenticate_new_password(username, password)  
            
            db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(f"/users/{user.id}/profile")
        else:
            return render_template('users/edit_password.html', form=form, user=user)
    
    return render_template('users/edit_password.html', form=form, user=user)


@app.route(f"/users/<int:user_id>/lessons")
def show_user_lessons(user_id):
    """Show a list of user lessons (seperate from user home which will show all scheduled lessons on a calendar. this will be a list of lessons)."""

    user = User.query.get(user_id)

    lessons = (Lesson.query.filter(Lesson.user_id == user_id).order_by(asc(Lesson.date)).all())
    
    return render_template('users/lessons.html', user=user, lessons=lessons)

@app.route(f"/users/<int:user_id>/resources")
def show_user_resources(user_id):
    """Show a list of user resources. page is only accessible to the logged in user."""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    resources = (Resource.query.filter(Resource.user_id == user_id).all())
    
    return render_template('users/resources.html', user=user, resources=resources)

@app.route('/users/<int:user_id>/following')
def show_following(user_id):
    """Show list of people this user is following."""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    return render_template('users/following.html', user=user)


@app.route('/users/<int:user_id>/followers')
def users_followers(user_id):
    """Show list of followers of this user."""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    return render_template('users/followers.html', user=user)

@app.route('/users/follow/<int:follow_id>', methods=['POST'])
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""

    user = User.query.get_or_404(session['id'])

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    followed_user = User.query.get_or_404(follow_id)
    user.following.append(followed_user)
    db.session.commit()

    return redirect(f"/users/{user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    user = User.query.get_or_404(session['id'])

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    followed_user = User.query.get(follow_id)
    user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{user.id}/following")



"""Lesson Routes"""



@app.route(f"/users/<int:user_id>/lessons/new", methods=['GET'])
def show_add_lesson_form(user_id):
    """show form for adding a lesson plan"""
    
    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = AddLessonForm()

    resources = [(resource.title, resource.url) for resource in Resource.query.filter(Resource.user_id == user.id).all()]

    form.resources.choices = resources

    return render_template("lessons/new.html", user=user, form=form, resources=resources)


@app.route(f"/users/<int:user_id>/lessons/new", methods=['POST'])
def handle_add_lesson_form(user_id):
    """Submit New Lesson plan and redirect to user home"""

    user = User.query.get(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = AddLessonForm()

    resources = [(resource.title, resource.url) for resource in Resource.query.filter(Resource.user_id == user.id).all()]

    form.resources.choices = resources

    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        date = form.add_lesson_date.data.strftime('%Y-%m-%d')
        resources = form.resources.data
        
        lesson = Lesson(
            title=title,
            summary=summary,
            date=date,
            user_id=user_id
        )

        db.session.add(lesson)
        db.session.commit()

        return redirect(f"/users/{user_id}/lessons")

    else:
        return render_template("lessons/new.html", user=user, form=form)

@app.route(f"/lessons/<int:lesson_id>")
def show_single_lesson(lesson_id):
    """Show information about a single lesson"""
    
    if "id" not in session:
        flash('Please login to view.')
        return redirect('/login')

    lesson = Lesson.query.get(lesson_id)
    user = User.query.get(lesson.user_id)

    return render_template('/lessons/detail.html', lesson=lesson, user=user)


@app.route(f"/lessons/<int:lesson_id>/edit", methods=['GET'])
def show_edit_lesson_form(lesson_id):
    """Show form to edit a lesson plan"""
    lesson = Lesson.query.get(lesson_id)
    user = User.query.get(lesson.user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditLessonForm(obj=lesson)

    resources = [(resource.title, resource.url) for resource in Resource.query.filter(Resource.user_id == user.id).all()]

    form.resources.choices = resources

    return render_template('/lessons/edit.html', lesson=lesson, user=user, form=form)


@app.route(f"/lessons/<int:lesson_id>/edit", methods=['POST'])
def handle_edit_lesson_form(lesson_id):
    """Handle submit of form to edit a lesson plan, redirect to the main page for the lesson"""
    lesson = Lesson.query.get(lesson_id)
    user = User.query.get(lesson.user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditLessonForm(obj=lesson)

    resources = [(resource.title, resource.url) for resource in Resource.query.filter(Resource.user_id == user.id).all()]

    form.resources.choices = resources

    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.summary = form.summary.data
        lesson.date = form.edit_lesson_date.data.strftime('%Y-%m-%d')
        for resource_title in form.resources.data:
            if lesson.resources:
                lesson.resources.append(Resource.query.get(resource_title))

        db.session.commit()

        return redirect(f"/lessons/{lesson.id}")

    return render_template("lessons/edit.html", form=form, lesson=lesson, user=user)

@app.route("/lessons/<int:lesson_id>/delete", methods=["POST"])
def delete_lesson(lesson_id):
    """Delete individual lesson."""

    lesson = Lesson.query.get(lesson_id)
    user = lesson.user
    
    if "id" not in session or lesson.user_id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    db.session.delete(lesson)
    db.session.commit()

    return redirect(f"/users/{user.id}/lessons")


"""Resource routes"""


@app.route("/users/<int:user_id>/resources/search", methods=['GET'])
def show_resource_search_page(user_id):
    """show resource search form, where js code will show search results from 3rd party API"""
    user = User.query.get_or_404(user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    return render_template("resources/search.html", user=user)

@app.route("/users/<int:user_id>/resources/search", methods=['POST'])
#use the package below when testing app in insomnia
#@csrf.exempt  
def handle_add_resource(user_id):
    """handle resource add form (dynamically created with js)"""
    user = User.query.get(user_id);

    if "id" not in session or user.id != session['id']:
       flash('Please login to view.')
       return redirect('/login')
    
    data = request.get_json(force=True)
    id = data['id']
    title = data["title"]
    description = data["description"]
    url = data["url"]

    new_resource = Resource(id=id, title=title, description=description, url=url, user_id=user.id)
    
    db.session.add(new_resource)
    db.session.commit()

    return redirect(f"/users/{user.id}/resources")


@app.route(f"/resources/<int:resource_numerical_id>")
def show_single_resource(resource_numerical_id):
    """Show information about a single resource"""
    
    if "id" not in session:
        flash('Please login to view.')
        return redirect('/login')

    resource = Resource.query.get(resource_numerical_id)
    user = User.query.get(resource.user_id)

    return render_template('/resources/detail.html', resource=resource, user=user)

@app.route("/resources/<int:resource_numerical_id>/edit", methods=["GET"])
def show_edit_resource_form(resource_numerical_id):
    """Show resource edit form"""
    resource = Resource.query.get(resource_numerical_id)
    user = User.query.get(resource.user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditResourceForm(obj=resource)

    lesson = [(lesson.id, lesson.title) for lesson in Lesson.query.filter(Lesson.user_id == user.id).all()]

    form.lesson.choices = lesson

    return render_template('/resources/edit.html', resource=resource, form=form, user=user)

@app.route(f"/resources/<int:resource_numerical_id>/edit", methods=['POST'])
def handle_edit_resource_form(resource_numerical_id):
    """Handle submit of form to edit a resource, redirect to the main page for resources"""
    resource = Resource.query.get(resource_numerical_id)
    user = User.query.get(resource.user_id)

    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    form = EditResourceForm(obj=resource)

    lesson = [(lesson.id, lesson.title) for lesson in Lesson.query.filter(Lesson.user_id == user.id).all()]

    form.lesson.choices = lesson

    if form.validate_on_submit():
        resource.title = form.title.data
        resource.description = form.description.data
        for lesson_title in form.lesson.data:
            if resource.lessons:
                resource.lessons.append(Lesson.query.get(lesson_title))

        db.session.commit()

        return redirect(f"/resources/{resource.numerical_id}")

    return render_template("resources/edit.html", form=form, resource=resource, user=user)

@app.route(f"/resources/<int:resource_numerical_id>/delete", methods=['POST'])
def delete_resource(resource_numerical_id):
    """Delete individual lesson."""

    resource = Resource.query.get(resource_numerical_id)
    user = User.query.get(session['id']);
    
    if "id" not in session or user.id != session['id']:
        flash('Please login to view.')
        return redirect('/login')

    db.session.delete(resource)
    db.session.commit()

    return redirect(f"/users/{user.id}/resources")


"""Common Error Handling"""


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

@app.errorhandler(503)
def service_unavailable(e):
    return render_template('errors/500.html'), 500









