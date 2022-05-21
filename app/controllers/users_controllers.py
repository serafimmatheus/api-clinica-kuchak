import email
from http import HTTPStatus
from flask import jsonify, request, current_app, session
from app.models.usuarios_models import UsuarioModel
from sqlalchemy.orm import Session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def create_users():
    session: Session = current_app.db.session
    data: dict = request.get_json()
    password_hash = data.pop("password")

    try:
        usuarios = UsuarioModel(**data)

        usuarios.password = password_hash

        session.add(usuarios)
        session.commit()

        return jsonify(usuarios), HTTPStatus.CREATED

    except TypeError:
        esperado = ["nome", "img_url", "email", "password"]
        obtido = [key for key in data.keys()]

        return {"esperado": esperado, "obtido": obtido}, HTTPStatus.BAD_REQUEST

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "email already exists!"}, HTTPStatus.CONFLICT

    except AttributeError as e:
        return {"error": f"{e}"}, HTTPStatus.BAD_REQUEST


@jwt_required()
def get_all_users():
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    users = session.query(UsuarioModel).filter_by(
        email=user_auth["email"]).first()

    if not users:
        return {"error": "user not found"}, HTTPStatus.NOT_FOUND

    return jsonify(users)


@jwt_required()
def get_user_by_id(user_id: int):
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    user_find_id = session.query(UsuarioModel).filter_by(
        email=user_auth["email"]).filter_by(id=user_id).first()

    if not user_find_id:
        return {"msg": "não autorizado!"}, HTTPStatus.UNAUTHORIZED

    return jsonify(user_find_id), HTTPStatus.OK


@jwt_required()
def update_users(user_id: int):
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    data: dict = request.get_json()
    user = session.query(UsuarioModel).filter_by(
        email=user_auth["email"]).filter_by(id=user_id).first()

    if not user:
        return {"msg": "Não autorizado"}, HTTPStatus.UNAUTHORIZED

    for key, value in data.items():
        setattr(user, key, value)

    data = {
        "id": user.id,
        "nome": user.nome,
        "img_url": user.img_url,
        "email": user.email
    }

    access_token = create_access_token(data)

    session.commit()

    return jsonify(user_auth, access_token), HTTPStatus.OK


@jwt_required()
def delete_user(user_id: int):
    session: Session = current_app.db.session

    user_auth = get_jwt_identity()

    user = session.query(UsuarioModel).filter_by(
        email=user_auth["email"]).filter_by(id=user_id).first()

    if not user:
        return {"error": "nao autorizado"}, HTTPStatus.UNAUTHORIZED

    session.delete(user)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
