from sqlalchemy import UniqueConstraint

from sqlalchemy import orm
from viggocore.database import db
from viggocore.common.subsystem import entity


class NCM_CEST(entity.Entity, db.Model):

    attributes = ['ncm_id', 'cest_id']
    attributes += entity.Entity.attributes

    ncm_id = db.Column(
        db.CHAR(32), db.ForeignKey('ncm.id'), nullable=False)
    ncm = orm.relationship(
        'NCM', backref=orm.backref('ncm_cest_ncm'))
    cest_id = db.Column(
        db.CHAR(32), db.ForeignKey('cest.id'), nullable=False)
    cest = orm.relationship(
        'CEST', backref=orm.backref('ncm_cest_cest'))

    __tablename__ = 'ncm_cest'

    __table_args__ = (
        UniqueConstraint('ncm_id', 'cest_id',
                         name='ncm_cest_ncm_id_cest_id_uk'),)

    def __init__(self, id, ncm_id, cest_id,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.ncm_id = ncm_id
        self.cest_id = cest_id

    @classmethod
    def individual(cls):
        return 'ncm_cest'
