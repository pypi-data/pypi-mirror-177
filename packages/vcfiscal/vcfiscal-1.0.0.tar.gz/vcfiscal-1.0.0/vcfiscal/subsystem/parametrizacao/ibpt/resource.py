from sqlalchemy import UniqueConstraint
from viggocore.database import db
from viggocore.common.subsystem import entity


class IBPT(entity.Entity, db.Model):

    attributes = ['data_ini', 'data_fim', 'chave', 'versao', 'fonte']
    attributes += entity.Entity.attributes

    data_ini = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    chave = db.Column(db.String(10), nullable=False)
    versao = db.Column(db.String(10), nullable=False)
    fonte = db.Column(db.String(100), nullable=False)

    __tablename__ = 'ibpt'
    __table_args__ = (
        UniqueConstraint('chave', 'versao', name='ibpt_chave_versao_uk'),)

    def __init__(self, id, data_ini, data_fim, chave, versao, fonte,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)

        self.data_ini = self.allDateFmtFromAllTypes(data_ini)
        self.data_fim = self.allDateFmtFromAllTypes(data_fim)
        self.chave = chave
        self.versao = versao
        self.fonte = fonte
