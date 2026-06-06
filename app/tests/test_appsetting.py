import unittest
from app import create_app
from app.extensions import db
from app.models import AppSetting
from flask import g

class AppSettingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        if hasattr(g, 'app_settings_cache'): del g.app_settings_cache
        self.app_context.pop()

    def test_caching(self):
        AppSetting.set('test_key', 'test_val')
        # Setting a value should populate the cache and store in DB
        self.assertTrue(hasattr(g, 'app_settings_cache'))
        self.assertEqual(g.app_settings_cache.get('test_key'), 'test_val')

        # Getting the value should use cache
        val = AppSetting.get('test_key')
        self.assertEqual(val, 'test_val')

        # Modify DB directly to bypass cache setter
        setting = AppSetting.query.filter_by(key='test_key').first()
        setting.value = 'new_val'
        db.session.commit()

        # Get should still return old value from cache
        val_cached = AppSetting.get('test_key')
        self.assertEqual(val_cached, 'test_val')

        # Pop context to simulate new request
        if hasattr(g, 'app_settings_cache'): del g.app_settings_cache
        self.app_context.pop()
        self.app_context.push()

        # Get should now return new value and hit DB to populate fresh cache
        val_fresh = AppSetting.get('test_key')
        self.assertEqual(val_fresh, 'new_val')

if __name__ == '__main__':
    unittest.main()
