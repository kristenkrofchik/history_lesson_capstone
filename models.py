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

    lessons = db.relationship('Lesson')

class Lesson(db.Model):
    """Lesson (Lesson Plan) Model"""

    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.Text, nullable=False)

    summary = db.Column(db.Text)

    start_date = db.Column(db.DateTime, nullable=False)

    end_date = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', secondary='users_lessons', backref=lessons)

    resources = db.relationship('Resource')

class UserLesson(db.Model):
    """Ties Between a User (Teacher) and their Lessons"""

    __tablename__ = "users_lessons"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), primary_key=True)

