from http import HTTPStatus
from flask import current_app, jsonify, request
from sqlalchemy.orm import Session
from app.models.clientes_models import ClientesModel
from flask_jwt_extended import jwt_required, get_jwt_identity


@jwt_required()
def create_clientes():
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    data: dict = request.get_json()

    data["user_id"] = user_auth["id"]

    cliente = ClientesModel(**data)

    session.add(cliente)
    session.commit()

    return jsonify(cliente), HTTPStatus.CREATED


@jwt_required()
def get_all_clientes():
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    clientes = session.query(ClientesModel).filter_by(user_id=user_auth["id"]).all()

    return jsonify(clientes), HTTPStatus.OK


@jwt_required()
def get_clientes_by_id(cliente_cpf: str):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    try:
        clientes = session.query(ClientesModel).filter_by(user_id=user_auth["id"]).filter_by(cpf=cliente_cpf).first()

        if not clientes:
            return {"error": f"{cliente_cpf} not found!"},HTTPStatus.NOT_FOUND
            
        return jsonify(clientes), HTTPStatus.OK
    except:
        return {"message": f"id {cliente_cpf} not found!"}, HTTPStatus.NOT_FOUND


@jwt_required()
def atualizando_clientes(cliente_cpf: str):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()
    data: dict = request.get_json()

    try:
        cliente_find_cpf = session.query(ClientesModel).filter_by(user_id=user_auth["id"]).filter_by(cpf=cliente_cpf).first()

        for key, value in data.items():
            setattr(cliente_find_cpf, key, value)

        session.commit()
    except:
        return {"error": "not found"}, HTTPStatus.NOT_FOUND

    return jsonify(cliente_find_cpf), HTTPStatus.OK


@jwt_required()
def delete_clientes(cliente_cpf: str):
    session: Session = current_app.db.session
    user_auth = get_jwt_identity()

    try:
        cliente_find_cpf = session.query(ClientesModel).filter_by(user_id=user_auth["id"]).filter_by(cpf=cliente_cpf).first()

        session.delete(cliente_find_cpf)
        session.commit()
    except:
        return {"error": "not found!"}, HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT



