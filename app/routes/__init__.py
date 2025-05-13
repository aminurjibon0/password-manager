from flask import Blueprint

auth = Blueprint('auth', __name__)
vault = Blueprint('vault', __name__)

from app.routes import auth, vault