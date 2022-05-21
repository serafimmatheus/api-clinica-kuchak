from dataclasses import dataclass
from app.configs.database import db
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id:int
    nome: str
    img_url: str
    email: str
    clientes: list

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    img_url = db.Column(db.String)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String)
    clientes = db.relationship("ClientesModel", back_populates="users")


    @property
    def password(self):
        raise AttributeError("Password cannot be accessed!")


    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)


    def verify_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

