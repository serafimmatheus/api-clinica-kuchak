from http import HTTPStatus
from flask import current_app, jsonify, request, session
from sqlalchemy.orm import Session, Query
from app.models.dogs_models import DogsModel
from app.models.clientes_models import ClientesModel
from app.models.usuarios_models import UsuarioModel
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def create_pets():
    session: Session = current_app.db.session
    data: dict = request.get_json()

    try:
        pets = DogsModel(**data)

        session.add(pets)
        session.commit()

        return jsonify(pets), HTTPStatus.CREATED
    except TypeError:
        esperado = ["raca", "nome", "data_nascimento", "pelagem", "is_castrado", "cliente_id"]
        obtido = [key for key in data.keys()]

        return {"esperado": esperado, "obtido": obtido}, HTTPStatus.BAD_REQUEST
    


@jwt_required()
def get_all_pets():
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    dogs: Query = (
        session
        .query(DogsModel)
        .select_from(DogsModel)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .order_by(DogsModel.id)
        .all()
    )

    return jsonify(dogs), HTTPStatus.OK


@jwt_required()
def get_pets_by_id(pet_id: int):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    dogs: Query = (
        session
        .query(DogsModel)
        .select_from(DogsModel)
        .filter_by(id=pet_id)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .first()
    )

    if not dogs:
        return {"error": "id not found!"}, HTTPStatus.NOT_FOUND


    return jsonify(dogs), HTTPStatus.OK


@jwt_required()
def atualizando_pets(pet_id: int):
    session: Session = current_app.db.session
    data = request.get_json()
    user_auth = get_jwt_identity()

    try:
        dogs: Query = (
            session
            .query(DogsModel)
            .select_from(DogsModel)
            .filter_by(id=pet_id)
            .join(ClientesModel)
            .join(UsuarioModel)
            .filter_by(id=user_auth["id"])
            .first()
        )

        for key, value in data.items():
            setattr(dogs, key, value)

        session.commit()

        return jsonify(dogs), HTTPStatus.OK
    except AttributeError:
        return {"error": "Unauthorized!"}, HTTPStatus.UNAUTHORIZED


@jwt_required()
def delete_pet_by_id(pet_id: int):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    dog: Query = (
        session
        .query(DogsModel)
        .select_from(DogsModel)
        .filter_by(id=pet_id)
        .join(ClientesModel)
        .join(UsuarioModel)
        .filter_by(id=user_auth["id"])
        .first()
    )

    if not dog:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    session.delete(dog)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
    