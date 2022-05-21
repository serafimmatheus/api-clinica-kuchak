from flask import Blueprint
from app.controllers import tipos_vacinas_controllers


bp = Blueprint("vacians", __name__, url_prefix="/users/clientes/pets/vacinas")


bp.get("")(tipos_vacinas_controllers.get_all_vacinas)
bp.get("/<int:vacina_id>")(tipos_vacinas_controllers.get_vacinas_by_id)
bp.post("")(tipos_vacinas_controllers.craete_vacinas)
bp.patch("/<int:vacina_id>")(tipos_vacinas_controllers.update_vacinas)
bp.delete("/<int:vacina_id>")(tipos_vacinas_controllers.delete_vacinas)