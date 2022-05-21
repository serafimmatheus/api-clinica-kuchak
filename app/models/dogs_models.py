from dataclasses import dataclass
from app.configs.database import db


@dataclass
class DogsModel(db.Model):
    __tablename__ = "dogs"

    id: int
    raca: str
    nome: str
    data_nascimento: str
    pelagem: str
    is_castrado: bool
    vacinas: list

    id = db.Column(db.Integer, primary_key=True)
    raca = db.Column(db.String(30), nullable=False)
    nome = db.Column(db.String(30), nullable=False)
    data_nascimento = db.Column(db.Date)
    pelagem = db.Column(db.String(50), nullable=False)
    is_castrado = db.Column(db.Boolean, nullable=False)
    cliente_id = db.Column(db.String, db.ForeignKey("clientes.cpf"), nullable=False)
    
    vacinas = db.relationship("TiposVacinasModel", backref="pet_vacina")
    
