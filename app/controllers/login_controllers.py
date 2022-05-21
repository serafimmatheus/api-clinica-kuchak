from http import HTTPStatus
from flask import current_app, request
from sqlalchemy.orm import Session
from app.models.usuarios_models import UsuarioModel
from flask_jwt_extended import create_access_token
from datetime import timedelta


def login():
    session: Session = current_app.db.session

    data = request.get_json()

    user: UsuarioModel = session.query(UsuarioModel).filter_by(email=data["email"]).first()

    if not user:
        return {"error": f"User not found"}, HTTPStatus.NOT_FOUND


    if user.verify_password(data["password"]):
        data = {
            "id":user.id,
            "nome": user.nome,
            "img_url": user.img_url,
            "email": user.email
        }

        access_token = create_access_token(identity=data, expires_delta=timedelta(days=1))
        return {"token": access_token, "user": data}, HTTPStatus.OK
    else:
        return {"error": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
        
