import unittest
from app import create_app, db
from app.models import AppSetting
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class SettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_settings_crud(self):
        # Test Get Default
        self.assertIsNone(AppSetting.get_value('non_existent'))
        self.assertEqual(AppSetting.get_value('non_existent', 'default'), 'default')

        # Test Set
        AppSetting.set_value('test_key', 'test_value')
        self.assertEqual(AppSetting.get_value('test_key'), 'test_value')

        # Test Update
        AppSetting.set_value('test_key', 'new_value')
        self.assertEqual(AppSetting.get_value('test_key'), 'new_value')

        # Test Persistency
        s = db.session.get(AppSetting, 'test_key')
        self.assertIsNotNone(s)
        self.assertEqual(s.value, 'new_value')

    def test_settings_multiple(self):
        AppSetting.set_value('k1', 'v1')
        AppSetting.set_value('k2', 'v2')
        self.assertEqual(AppSetting.get_value('k1'), 'v1')
        self.assertEqual(AppSetting.get_value('k2'), 'v2')
