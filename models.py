from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follows(db.Model):
    """Followers and Following relationships"""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)

    user_following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)


class User(db.Model):
    """User/Teacher Model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    username = db.Column(db.Text, nullable=False, unique=True)
    
    password = db.Column(db.Text, nullable=False)
    
    email = db.Column(db.Text, nullable=False, unique=True)
    
    first_name = db.Column(db.Text)
    
    last_name = db.Column(db.Text)
    
    school = db.Column(db.Text)
    
    grade = db.Column(db.Text)
    
    location = db.Column(db.Text)

    following = db.relationship("User", secondary="follows", 
        primaryjoin=(Follows.user_following_id == id), 
        secondaryjoin=(Follows.user_being_followed_id == id)
    )

    followers = db.relationship("User", secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    lesson = db.relationship("Lesson", backref="user", cascade="all,delete")

    @classmethod
    def signup(cls, username, password, email):
        """Signs up user for profile.

        Hashes password and adds user to database.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
        )

        db.session.add(user)
        return user

    
    @classmethod
    def authenticate(cls, username, password):
        """Finds user with given username and password.

        Searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user. If it doesn't 
        find matching user (or if the password is incorrect), it will return False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    @classmethod
    def authenticate_new_password(cls, username, password):
        """security for password change"""

        user = cls.query.filter_by(username=username).first()

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        if user:
            user.password = hashed_pwd

            db.session.add(user)
            db.session.commit

            return user


    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1


class Lesson(db.Model):
    """Lesson (Lesson Plan) Model"""

    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    summary = db.Column(db.Text)

    date = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)


class UserLesson(db.Model):
    """Ties Between a User (Teacher) and their Lessons"""

    __tablename__ = "users_lessons"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), primary_key=True)


class Resource(db.Model):
    """Model for resource from LOC API"""

    __tablename__ = "resources"

    id = db.Column(db.Text, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    description = db.Column(db.Text)

    url = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    lesson = db.relationship('Lesson', secondary='lessons_resources', backref='resources')


class LessonResource(db.Model):
    """Ties Between a lesson and its resources"""

    __tablename__ = "lessons_resources"

    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), primary_key=True)
    
    resource_id = db.Column(db.Text, db.ForeignKey('resources.id'), primary_key=True)

def serialize_user(user):
        """Serialize a dessert SQLAlchemy obj to dictionary."""

        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "school": user.school,
            "grade": user.grade,
            "location": user.location
        }

def serialize_lesson(lesson):
        """Serialize a dessert SQLAlchemy obj to dictionary."""

        return {
            "id": lesson.id,
            "title": lesson.title,
            "summary": lesson.summary,
            "date": lesson.date,
            "user_id": lesson.user_id
        }

def serialize_resource(resource):
        """Serialize a dessert SQLAlchemy obj to dictionary."""

        return {
            "id": resource.id,
            "title": resource.title,
            "description": resource.description,
            "url": resource.url
        }

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)




