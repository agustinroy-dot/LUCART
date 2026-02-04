from flask import Blueprint

suppliers_bp = Blueprint('suppliers', __name__)

from app.suppliers import routes
