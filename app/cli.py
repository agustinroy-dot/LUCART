import click
from flask.cli import with_appcontext
from app import db
from app.models import Customer, Material, User, Order, Transaction
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

@click.command(name='seed')
@with_appcontext
def seed():
    """Seeds the database with demo data."""

    # Check if data exists
    if User.query.first():
        print("Data already exists. Skipping seed.")
        return

    print("Seeding database...")

    # Admin
    admin = User(username='admin')
    admin.set_password('admin')
    db.session.add(admin)

    # Customers
    c1 = Customer(name="TechStart Inc.", email="contact@techstart.com", phone="555-0101", address="123 Tech Blvd")
    c2 = Customer(name="John Doe (Hobbyist)", email="john.doe@email.com", phone="555-0102")
    db.session.add_all([c1, c2])
    db.session.commit()

    # Materials
    m1 = Material(name="PLA Black (Generic)", type="Filament", quantity=2500, unit="g", cost=0.02, min_stock=1000)
    m2 = Material(name="PLA White (Generic)", type="Filament", quantity=800, unit="g", cost=0.02, min_stock=1000) # Low stock
    m3 = Material(name="Resin Grey (Elegoo)", type="Resin", quantity=2, unit="L", cost=30.0, min_stock=1)
    db.session.add_all([m1, m2, m3])
    db.session.commit()

    # Orders
    o1 = Order(customer_id=c1.id, description="Prototype Casing V2", price=150.00, status="In Production", date_created=datetime.utcnow(), date_due=datetime.utcnow() + timedelta(days=2))
    o2 = Order(customer_id=c2.id, description="Miniature Figurine", price=25.00, status="Pending", date_created=datetime.utcnow(), date_due=datetime.utcnow() + timedelta(days=5))
    db.session.add_all([o1, o2])
    db.session.commit()

    # Transactions
    t1 = Transaction(date=datetime.utcnow() - timedelta(days=10), type='expense', category='Material', amount=200.0, description="Filament Restock", is_business=True)
    t2 = Transaction(date=datetime.utcnow() - timedelta(days=5), type='income', category='Sales', amount=500.0, description="Bulk Order Pay", is_business=True)
    db.session.add_all([t1, t2])
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
