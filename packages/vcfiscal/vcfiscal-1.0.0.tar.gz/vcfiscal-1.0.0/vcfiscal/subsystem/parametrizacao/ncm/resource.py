from sqlalchemy import UniqueConstraint

from viggocore.database import db
from viggocore.common.subsystem import entity


class NCM(entity.Entity, db.Model):

    attributes = ['codigo', 'ex', 'descricao', 'tipo', 'cest_id']
    attributes += entity.Entity.attributes

    codigo = db.Column(db.CHAR(9), nullable=False)
    ex = db.Column(db.VARCHAR(2), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.Numeric(1), nullable=False)

    __tablename__ = 'ncm'

    __table_args__ = (
        UniqueConstraint('codigo', 'ex', name='ncm_codigo_ex_uk'),)

    def __init__(self, id, codigo, descricao, tipo, ex='', cest_id=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.cest_id = cest_id
        self.codigo = codigo
        self.ex = ex
        self.descricao = descricao
        self.tipo = tipo
