from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    quotes = db.relationship('Quote', backref='customer', lazy='dynamic')

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, nullable=False)
    type = db.Column(db.String(50)) # PLA, Resin, Component, etc.
    quantity = db.Column(db.Float, default=0.0)
    unit = db.Column(db.String(20)) # g, kg, L, units
    cost = db.Column(db.Float, default=0.0) # Cost per unit
    min_stock = db.Column(db.Float, default=0.0)

    logs = db.relationship('InventoryLog', backref='material', lazy='dynamic')
    order_usages = db.relationship('OrderMaterial', backref='material', lazy='dynamic')

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    change_amount = db.Column(db.Float)
    type = db.Column(db.String(20)) # 'in', 'out', 'adjustment'
    reason = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20)) # 'income', 'expense'
    category = db.Column(db.String(50))
    amount = db.Column(db.Float)
    description = db.Column(db.String(200))
    is_business = db.Column(db.Boolean, default=True)

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Draft') # Draft, Sent, Accepted, Rejected
    total = db.Column(db.Float, default=0.0)
    notes = db.Column(db.Text)

    items = db.relationship('QuoteItem', backref='quote', lazy='dynamic', cascade='all, delete-orphan')

class QuoteItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))
    description = db.Column(db.String(200))
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, default=0.0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending') # Pending, In Production, Finished, Delivered, Cancelled
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_due = db.Column(db.DateTime)
    price = db.Column(db.Float, default=0.0)
    payment_status = db.Column(db.String(20), default='Pending') # Pending, Paid, Deposit

    materials = db.relationship('OrderMaterial', backref='order', lazy='dynamic', cascade='all, delete-orphan')

class OrderMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'))
    quantity_estimated = db.Column(db.Float, default=0.0)
    quantity_real = db.Column(db.Float, default=0.0)

class AppSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(120))
    address = db.Column(db.String(200))
    cuit = db.Column(db.String(20))
