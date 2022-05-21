from dataclasses import dataclass
from app.configs.database import db


@dataclass
class ClientesModel(db.Model):
    __tablename__ = "clientes"

    cpf: str
    nome: str
    email: str
    telefone: str
    endereco: str
    is_whatsapp: bool
    dogs: list
    cats: list

    cpf = db.Column(db.String(11), primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(14), nullable=False, unique=True)
    endereco = db.Column(db.String(50), nullable=False)
    is_whatsapp = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    users = db.relationship("UsuarioModel", back_populates="clientes")
    dogs = db.relationship("DogsModel", backref="pet")
    cats = db.relationship("CatsModel", backref="cat")
