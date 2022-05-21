from flask import Blueprint
from app.controllers import dogs_controllers


bp = Blueprint("dogs", __name__, url_prefix="/users/clientes/dogs")


bp.get("")(dogs_controllers.get_all_pets)
bp.get("/<int:pet_id>")(dogs_controllers.get_pets_by_id)
bp.post("")(dogs_controllers.create_pets)
bp.patch("/<int:pet_id>")(dogs_controllers.atualizando_pets)
bp.delete("/<int:pet_id>")(dogs_controllers.delete_pet_by_id)