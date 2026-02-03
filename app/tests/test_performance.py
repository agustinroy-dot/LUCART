import unittest
from app import create_app, db
from app.models import User, Customer, Order, Quote
from config import Config
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class PerformanceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create User and Login
        u = User(username='test_user')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

        self.client.post('/auth/login', data={
            'username': 'test_user',
            'password': 'password'
        }, follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_orders_n_plus_one(self):
        # Create 10 customers and 10 orders
        for i in range(10):
            c = Customer(name=f"Customer {i}", email=f"c{i}@example.com")
            db.session.add(c)
            db.session.commit()

            o = Order(
                customer_id=c.id,
                description=f"Order {i}",
                status="Pending",
                date_created=datetime.utcnow()
            )
            db.session.add(o)
        db.session.commit()

        query_count = 0
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            nonlocal query_count
            # Ignore unrelated queries (like user loading if cached, or session)
            if "SELECT customer" in str(statement) or "SELECT order" in str(statement):
                query_count += 1
                # print(f"DEBUG QUERY: {statement}")

        event.listen(Engine, "before_cursor_execute", before_cursor_execute)

        try:
            self.client.get('/orders/')
        finally:
            event.remove(Engine, "before_cursor_execute", before_cursor_execute)

        print(f"Orders Index Queries (Relevant): {query_count}")
        # Optimized: Should be 1 query (joined)
        self.assertLess(query_count, 5, "Should not have N+1 queries for orders")

    def test_quotes_n_plus_one(self):
        # Create 10 customers and 10 quotes
        for i in range(10):
            c = Customer(name=f"Customer Q{i}", email=f"cq{i}@example.com")
            db.session.add(c)
            db.session.commit()

            q = Quote(
                customer_id=c.id,
                notes=f"Quote {i}",
                date=datetime.utcnow()
            )
            db.session.add(q)
        db.session.commit()

        query_count = 0
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            nonlocal query_count
            if "SELECT customer" in str(statement) or "SELECT quote" in str(statement):
                query_count += 1

        event.listen(Engine, "before_cursor_execute", before_cursor_execute)

        try:
            self.client.get('/quotes/')
        finally:
            event.remove(Engine, "before_cursor_execute", before_cursor_execute)

        print(f"Quotes Index Queries (Relevant): {query_count}")
        # Optimized: Should be 1 query (joined)
        self.assertLess(query_count, 5, "Should not have N+1 queries for quotes")
