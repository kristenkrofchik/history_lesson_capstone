"""User model tests."""

from datetime import date
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Lesson, User

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "password", "email1@email.com")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "password2", "email2@email.com")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_lesson_model(self):
        """Test basic model"""

        l = Lesson(
            title="Illinois History",
            date="2021-12-12",
            user_id=2222
        )

        db.session.add(l)
        db.session.commit()

        self.assertEqual(len(self.u2.lesson), 1)
    
   