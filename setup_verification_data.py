from app import create_app, db
from app.models import User, Customer, Order, Material, OrderMaterial

app = create_app('development')
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        u = User(username='admin')
        u.set_password('admin')
        db.session.add(u)

    if not Customer.query.filter_by(name='Verify Customer').first():
        c = Customer(name='Verify Customer', email='verify@example.com')
        db.session.add(c)
        db.session.commit()

        o = Order(customer_id=c.id, description='Verify Order', price=100.0)
        db.session.add(o)
        db.session.commit()

        m = Material(name='Verify Material', unit='kg', quantity=10.0)
        db.session.add(m)
        db.session.commit()

        om = OrderMaterial(order_id=o.id, material_id=m.id, quantity_estimated=2.0)
        db.session.add(om)
        db.session.commit()

    print("Data seeded.")
