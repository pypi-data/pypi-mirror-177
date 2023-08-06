from viggocore.database import db
from viggocore.common.subsystem import entity


class CFOP(entity.Entity, db.Model):

    attributes = ['codigo', 'descricao']
    attributes += entity.Entity.attributes

    codigo = db.Column(db.Numeric(4), unique=True, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(200), nullable=False)
    aplicacao = db.Column(db.String(1000), nullable=False)

    __tablename__ = 'cfop'

    def __init__(self, id, codigo, descricao, tipo, categoria, aplicacao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.codigo = codigo
        self.descricao = descricao
        self.tipo = tipo
        self.categoria = categoria
        self.aplicacao = aplicacao
