"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_user_repr(self):
        """Does the repr method work?"""
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        self.assertEqual(u.__repr__(), "<User #1: testuser, test@test.com>")

    def test_is_following(self):
        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        follow1 = Follows(user_being_followed_id=1, user_following_id=2)

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(follow1)
        db.session.commit()

        self.assertTrue(user2.is_following(user1))
        self.assertFalse(user1.is_following(user2))

    def test_is_followed_by(self):
        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        follow1 = Follows(user_being_followed_id=1, user_following_id=2)

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(follow1)
        db.session.commit()

        self.assertFalse(user2.is_followed_by(user1))
        self.assertTrue(user1.is_followed_by(user2))

    def test_user_create(self):
        user = User.signup(username='username', email='username@email.com', password='password', image_url='http://www.dfgsdfg.com')
        self.assertTrue(user)

        self.assertRaises(ValueError, User.signup(email='email'))

    def test_user_auth(self):
        user = User.signup(username='test_user', email='username@email.com', password='testpass', image_url='http://www.dfgsdfg.com')
        db.session.commit()

        self.assertTrue(User.authenticate(username="testuser", password="testpass"))
        self.assertFalse(User.authenticate(username="testuser", password="password"))
        self.assertFalse(User.authenticate(username="user", password="testpass"))




