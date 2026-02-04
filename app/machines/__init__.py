from flask import Blueprint

machines_bp = Blueprint('machines', __name__)

from app.machines import routes
