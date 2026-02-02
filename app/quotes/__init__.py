from flask import Blueprint

quotes_bp = Blueprint('quotes', __name__)

from app.quotes import routes
