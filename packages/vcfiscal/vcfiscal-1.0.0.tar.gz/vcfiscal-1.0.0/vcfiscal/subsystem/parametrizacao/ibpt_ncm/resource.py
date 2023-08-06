from sqlalchemy import orm, UniqueConstraint

from viggocore.common.subsystem import entity
from viggocore.database import db


class IBPTNCM(entity.Entity, db.Model):

    attributes = ['ibpt_id', 'ncm_id', 'sigla_uf', 'aliq_nac_fed',
                  'aliq_imp_fed', 'aliq_est', 'aliq_mun']
    attributes += entity.Entity.attributes

    ibpt_id = db.Column(
        db.CHAR(32), db.ForeignKey("ibpt.id"), nullable=False)
    ibpt = orm.relationship("IBPT", backref=orm.backref('ibpt_ncm_ibpt'))
    ncm_id = db.Column(
        db.CHAR(32), db.ForeignKey("ncm.id"), nullable=False)
    ncm = orm.relationship("NCM", backref=orm.backref('ibpt_ncm_ncm'))
    sigla_uf = db.Column(db.CHAR(2), nullable=False)
    aliq_nac_fed = db.Column(db.Numeric(6, 2), nullable=False)
    aliq_imp_fed = db.Column(db.Numeric(6, 2), nullable=False)
    aliq_est = db.Column(db.Numeric(6, 2), nullable=False)
    aliq_mun = db.Column(db.Numeric(6, 2), nullable=False)

    __tablename__ = 'ibpt_ncm'
    __table_args__ = (UniqueConstraint(
        'ibpt_id', 'ncm_id', 'sigla_uf',
        name='ibpt_ncm_ibpt_id_ncm_id_sigla_uf_uk'),)

    def __init__(self, id, ibpt_id, ncm_id, sigla_uf, aliq_nac_fed,
                 aliq_imp_fed, aliq_est, aliq_mun, active=True, created_at=None,
                 created_by=None, updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.ibpt_id = ibpt_id
        self.ncm_id = ncm_id
        self.sigla_uf = sigla_uf
        self.aliq_nac_fed = aliq_nac_fed
        self.aliq_imp_fed = aliq_imp_fed
        self.aliq_est = aliq_est
        self.aliq_mun = aliq_mun

    @classmethod
    def individual(cls):
        return 'ibpt_ncm'
