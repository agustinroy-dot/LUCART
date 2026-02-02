from flask import Flask
from config import config
from app.extensions import db, migrate, login
import os

def create_app(config_name='default'):
    app = Flask(__name__)

    # Load config
    if not isinstance(config_name, str):
        # Allow passing actual class object for testing
        app.config.from_object(config_name)
    else:
        app.config.from_object(config[config_name])

    # ProxyFix for production
    if app.config.get('use_proxy_fix'):
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Register CLI commands
    from app.cli import seed
    app.cli.add_command(seed)

    # Register Blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.finance import finance_bp
    app.register_blueprint(finance_bp, url_prefix='/finance')

    from app.inventory import inventory_bp
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    from app.orders import orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')

    from app.quotes import quotes_bp
    app.register_blueprint(quotes_bp, url_prefix='/quotes')

    from app.customers import customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    from app.settings import settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')

    from app.models import User # Import models to ensure they are registered with SQLAlchemy

    # Main route (Dashboard)
    from flask import render_template
    from flask_login import login_required
    from app.models import Order, Material, Transaction
    from datetime import datetime
    from sqlalchemy import extract

    # Error Handling
    from flask import render_template

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # Logging
    if not app.debug:
        from app.errors import configure_logging
        configure_logging(app)

    @app.route('/')
    @login_required
    def index():
        # Stats
        pending_orders = Order.query.filter_by(status='Pending').count()
        production_orders = Order.query.filter_by(status='In Production').count()

        low_stock_items = [m for m in Material.query.all() if m.quantity <= m.min_stock]

        now = datetime.now()
        income_month = db.session.query(db.func.sum(Transaction.amount)).filter(
            extract('year', Transaction.date) == now.year,
            extract('month', Transaction.date) == now.month,
            Transaction.type == 'income'
        ).scalar() or 0

        expense_month = db.session.query(db.func.sum(Transaction.amount)).filter(
            extract('year', Transaction.date) == now.year,
            extract('month', Transaction.date) == now.month,
            Transaction.type == 'expense'
        ).scalar() or 0

        return render_template('index.html',
            pending_orders_count=pending_orders,
            production_orders_count=production_orders,
            low_stock_items=low_stock_items,
            income_month=income_month,
            expense_month=expense_month,
            now=now
        )

    return app
