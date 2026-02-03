import unittest
from app import create_app, db
from app.models import User, Transaction
from config import Config
from datetime import datetime

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class FinanceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create user
        u = User(username='test')
        u.set_password('pass')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def test_finance_index_calculations(self):
        self.login('test', 'pass')

        # Add transactions for current month
        t1 = Transaction(date=datetime.now(), type='income', amount=100.0, is_business=True, description='T1', category='cat')
        t2 = Transaction(date=datetime.now(), type='expense', amount=40.0, is_business=True, description='T2', category='cat')
        t3 = Transaction(date=datetime.now(), type='income', amount=50.0, is_business=False, description='T3', category='cat')

        db.session.add_all([t1, t2, t3])
        db.session.commit()

        # Test Default (Business)
        response = self.client.get('/finance/')
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('00.0', content)
        self.assertIn('0.0', content)
        self.assertIn('0.0', content) # Balance

        # Test Scope All
        response = self.client.get('/finance/?scope=all')
        self.assertEqual(response.status_code, 200)
        content = response.get_data(as_text=True)
        self.assertIn('50.0', content)
        self.assertIn('0.0', content)
        self.assertIn('10.0', content)
