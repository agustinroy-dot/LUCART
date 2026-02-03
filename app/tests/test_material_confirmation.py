import unittest
from app import create_app, db
from app.models import User, Customer, Material, Order, OrderMaterial, InventoryLog
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class MaterialConfirmationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create User
        self.u = User(username='admin')
        self.u.set_password('password')
        db.session.add(self.u)
        db.session.commit()

        # Login
        self.client.post('/auth/login', data={
            'username': 'admin',
            'password': 'password'
        }, follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_material_deduction_flow(self):
        # 1. Setup Data
        c = Customer(name="Test Customer")
        db.session.add(c)

        m = Material(name="PLA Black", quantity=1000.0, unit="g")
        db.session.add(m)
        db.session.commit()

        o = Order(customer_id=c.id, description="Test Order")
        db.session.add(o)
        db.session.commit()

        om = OrderMaterial(order_id=o.id, material_id=m.id, quantity_estimated=100.0, quantity_real=0.0)
        db.session.add(om)
        db.session.commit()

        # 2. Test GET Confirmation Page
        resp = self.client.get(f'/orders/material/{om.id}/deduct', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Confirm Material Usage', resp.data)
        self.assertIn(b'value="100.0"', resp.data) # Check pre-fill

        # 3. Test POST Confirmation (Update Real Quantity to 110.0)
        resp = self.client.post(f'/orders/material/{om.id}/deduct', data={
            'quantity_real': 110.0
        }, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Stock deducted successfully (110.0 g)', resp.data)

        # 4. Verify DB State
        # Need to query in a fresh session or refresh
        db.session.expire_all()

        om_check = OrderMaterial.query.get(om.id)
        self.assertEqual(om_check.quantity_real, 110.0)

        m_check = Material.query.get(m.id)
        self.assertEqual(m_check.quantity, 1000.0 - 110.0) # 890.0

        log = InventoryLog.query.filter_by(material_id=m.id).first()
        self.assertIsNotNone(log)
        self.assertEqual(log.change_amount, 110.0)
        self.assertEqual(log.type, 'out')

        # 5. Test Idempotency (Try to deduct again)
        resp = self.client.get(f'/orders/material/{om.id}/deduct', follow_redirects=True)
        self.assertIn(b'Material already deducted', resp.data)

        # Verify no double deduction
        db.session.expire_all()
        m_check_2 = Material.query.get(m.id)
        self.assertEqual(m_check_2.quantity, 890.0)

if __name__ == '__main__':
    unittest.main()
