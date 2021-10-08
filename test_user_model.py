"""User model tests."""

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User

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


    def test_user_model(self):
        """Test basic model"""

        u = User(
            email="test@test.com",
            password="HASHED_PASSWORD",
            username="testuser"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no followers & no users they are following 
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(len(u.following), 0)
    
    def test_valid_register(self):
        """Test valid registration"""
        u_test = User.signup("testtesttest", "password", "testtest@test.com")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
    
    def test_invalid_register(self):
        """Test invalid registration"""
        invalid_u = User.signup(None, 'thebestpassword', None)
        uid = 1234567
        invalid_u.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_valid_login(self):
        """Test valid login"""
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_login(self):
        """Test invalid login"""
        self.assertFalse(User.authenticate("badusername", "password"))
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))