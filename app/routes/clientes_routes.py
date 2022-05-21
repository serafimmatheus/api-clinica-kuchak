from flask import Blueprint
from app.controllers import clientes_controllers


bp = Blueprint("clientes", __name__, url_prefix="/users/clientes")


# clientes
bp.get("")(clientes_controllers.get_all_clientes)
bp.get("/<cliente_cpf>")(clientes_controllers.get_clientes_by_id)
bp.post("")(clientes_controllers.create_clientes)
bp.patch("/<cliente_cpf>")(clientes_controllers.atualizando_clientes)
bp.delete("/<cliente_cpf>")(clientes_controllers.delete_clientes)