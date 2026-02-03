import unittest
from app import create_app, db
from app.models import User, Customer, Order, Material, OrderMaterial
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class OrderMaterialsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create User
        u = User(username='test_user')
        u.set_password('password')
        db.session.add(u)

        # Create Data
        c = Customer(name="Test Customer")
        db.session.add(c)

        m = Material(name="Test Material", unit="kg", quantity=100)
        db.session.add(m)

        db.session.commit()

        # Store IDs
        self.customer_id = c.id
        self.material_id = m.id

        o = Order(customer_id=c.id, description="Test Order")
        db.session.add(o)
        db.session.commit()
        self.order_id = o.id

        # Login
        self.client.post('/auth/login', data={
            'username': 'test_user',
            'password': 'password'
        }, follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_duplicate_material_prevention(self):
        # 1. Add Material First Time
        response = self.client.post(f'/orders/{self.order_id}', data={
            'material_id': self.material_id,
            'quantity': 10
        }, follow_redirects=True)

        # Check if added
        om = OrderMaterial.query.filter_by(order_id=self.order_id, material_id=self.material_id).first()
        self.assertIsNotNone(om, "Material should be added initially")
        self.assertEqual(om.quantity_estimated, 10)

        # 2. Add Same Material Second Time
        response = self.client.post(f'/orders/{self.order_id}', data={
            'material_id': self.material_id,
            'quantity': 5
        }, follow_redirects=True)

        # Check for error message in response
        response_text = response.get_data(as_text=True)
        self.assertIn("Este material ya ha sido agregado al pedido.", response_text, "Should show error message")

        # Verify quantity didn't change (still 10, not 15 or 5)
        oms = OrderMaterial.query.filter_by(order_id=self.order_id, material_id=self.material_id).all()
        self.assertEqual(len(oms), 1, "Should not add duplicate row")
        self.assertEqual(oms[0].quantity_estimated, 10, "Should not update existing quantity")

if __name__ == '__main__':
    unittest.main()
