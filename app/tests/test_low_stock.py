import unittest
from app import create_app, db
from app.models import Material
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class LowStockTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_low_stock_filtering(self):
        # Case 1: Quantity > Min Stock (Not Low)
        m1 = Material(name="Mat1", quantity=100, min_stock=10)
        # Case 2: Quantity == Min Stock (Low)
        m2 = Material(name="Mat2", quantity=10, min_stock=10)
        # Case 3: Quantity < Min Stock (Low)
        m3 = Material(name="Mat3", quantity=5, min_stock=10)

        db.session.add_all([m1, m2, m3])
        db.session.commit()

        # Replicate the logic currently in app/__init__.py
        # Current Logic:
        low_stock_current = [m for m in Material.query.all() if m.quantity <= m.min_stock]

        # Proposed Logic:
        low_stock_proposed = Material.query.filter(Material.quantity <= Material.min_stock).all()

        # Verify both logic sets return correct items (m2 and m3)
        expected_ids = {m2.id, m3.id}

        current_ids = {m.id for m in low_stock_current}
        proposed_ids = {m.id for m in low_stock_proposed}

        self.assertEqual(current_ids, expected_ids, "Current logic failed")
        self.assertEqual(proposed_ids, expected_ids, "Proposed logic failed")
