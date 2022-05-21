from flask import Blueprint
from app.controllers import users_controllers
from app.controllers import clientes_controllers


bp = Blueprint("users", __name__, url_prefix="/users")


bp.get("")(users_controllers.get_all_users)
bp.get("/<int:user_id>")(users_controllers.get_user_by_id)
bp.post("")(users_controllers.create_users)
bp.patch("/<int:user_id>")(users_controllers.update_users)
bp.delete("/<int:user_id>")(users_controllers.delete_user)
