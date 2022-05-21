from flask import Blueprint
from app.controllers import login_controllers


bp = Blueprint("login", __name__, url_prefix="/login")


bp.post("")(login_controllers.login)
