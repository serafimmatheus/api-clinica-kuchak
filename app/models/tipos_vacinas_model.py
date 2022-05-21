from dataclasses import dataclass
from app.configs.database import db


@dataclass
class TiposVacinasModel(db.Model):
    __tablename__ = "tipos_vacinas"

    id: int
    nome: str
    descricao: str
    data_aplicacao: str
    data_revacinacao: str
    is_pupies: bool

    id = db.Column(db.BigInteger, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.Text)
    data_aplicacao = db.Column(db.Date)
    data_revacinacao = db.Column(db.Date)
    is_pupies = db.Column(db.Boolean, default=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("dogs.id"))
    cat_id = db.Column(db.Integer, db.ForeignKey("cats.id"))
