import unittest
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from DashboardProject import db, create_app
from DashboardProject.models import User


class AccountSettingsTestCase(unittest.TestCase):
    def setUp(self):
        # can put 'testing' in the create app method if have different options for runnign app, eg, production, testing, dev
        self.app = create_app()
        self.client = self.app.test_client
        self.user_data = {
            'firstname': 'Test',
            'lastname': 'User',
            'curremail': 'test@example.com',
            'currpass': 'password',
            'newpass': 'newpassword'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()
            hashed_password = generate_password_hash(self.user_data['currpass'], method='pbkdf2:sha256')
            user = User(email=self.user_data['curremail'], password=hashed_password)
            db.session.add(user)
            db.session.commit()

    def test_account_settings(self):
        with self.app.app_context():
            res = self.client().post('/accountSetting', data=self.user_data)
            self.assertEqual(res.status_code, 200)
            user = User.query.filter_by(email=self.user_data['curremail']).first()
            self.assertTrue(user.check_password(self.user_data['newpass']))
"""
    ONLY TO BE USED WITH A TEST DATABASE
    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.drop_all()
"""

# runs the unit tests in the module
if __name__ == '__main__':
  unittest.main()
