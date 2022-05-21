from http import HTTPStatus
from flask import current_app, jsonify, request
from sqlalchemy.orm import Session, Query
from app.models.cats_models import CatsModel
from app.models.clientes_models import ClientesModel
from app.models.usuarios_models import UsuarioModel
from flask_jwt_extended import get_jwt_identity, jwt_required


def create_cats():
    session: Session = current_app.db.session
    data: dict = request.get_json()

    try:
        cat = CatsModel(**data)

        session.add(cat)
        session.commit()

        return jsonify(cat), HTTPStatus.CREATED

    except TypeError:
        esperado = ["raca", "nome", "data_nascimento", "pelagem", "is_castrado", "is_testado", "cliente_id"]
        obtido = [key for key in data.keys()]

        return {"esperado": esperado, "obtido": obtido}, HTTPStatus.BAD_REQUEST


@jwt_required()
def get_all_cats():
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    cats: Query = (
        session
        .query(CatsModel)
        .select_from(CatsModel)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .all())

    if not cats:
        return jsonify([]), HTTPStatus.OK

    return jsonify(cats), HTTPStatus.OK


@jwt_required()
def get_cats_by_id(cat_id: int):
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    cats: Query = (
        session
        .query(CatsModel)
        .select_from(CatsModel)
        .filter_by(id=cat_id)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .first()
    )

    if not cats:
        return jsonify({"error": "id not found!"}), HTTPStatus.NOT_FOUND


    return jsonify(cats), HTTPStatus.OK


@jwt_required()
def update_cats_by_id(cat_id: int):
    session: Session = current_app.db.session
    data: dict = request.get_json()
    user_auth = get_jwt_identity()

    cat: Query = (
        session
        .query(CatsModel)
        .select_from(CatsModel)
        .filter_by(id=cat_id)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .first()
    )

    if not cat:
        return {"error": "id not found!"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(cat, key, value)

    session.commit()

    return jsonify(cat)


@jwt_required()
def delete_cats_by_id(cat_id: int):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    cat: Query = (
        session
        .query(CatsModel)
        .select_from(CatsModel)
        .filter_by(id=cat_id)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .first()
    )

    if not cat:
        return {"error": "id not found!"}, HTTPStatus.NOT_FOUND

    session.delete(cat)
    session.commit()

    return "", HTTPStatus.NO_CONTENT

    