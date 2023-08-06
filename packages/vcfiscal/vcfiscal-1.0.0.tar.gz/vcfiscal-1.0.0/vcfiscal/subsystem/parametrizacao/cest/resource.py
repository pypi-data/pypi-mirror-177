from viggocore.database import db
from viggocore.common.subsystem import entity


class CEST(entity.Entity, db.Model):

    attributes = ['codigo', 'segmento', 'descricao']
    attributes += entity.Entity.attributes

    codigo = db.Column(db.CHAR(7), unique=True, nullable=False)
    segmento = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

    __tablename__ = 'cest'

    def __init__(self, id, codigo, segmento, descricao,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.codigo = codigo
        self.segmento = segmento
        self.descricao = descricao
