import enum

from sqlalchemy.types import Enum

from viggocore.common.subsystem import entity
from viggocore.database import db


class REGIME_PIS_COFINS(enum.Enum):
    CUMULATIVO = 0
    NAO_CUMULATIVO = 1
    MEI = 2
    SIMPLES = 3


class RegimeTributario(entity.Entity, db.Model):
    attributes = ['domain_id', 'crt', 'descricao', 'regime_pis_cofins',
                  'aliq_pis', 'aliq_cofins', 'contrib_ipi']
    attributes += entity.Entity.attributes

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey('domain.id'), nullable=False)
    crt = db.Column(db.Numeric(1), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    regime_pis_cofins = db.Column(Enum(REGIME_PIS_COFINS), nullable=False)
    aliq_pis = db.Column(db.Numeric(5, 2), nullable=True)
    aliq_cofins = db.Column(db.Numeric(5, 2), nullable=True)
    contrib_ipi = db.Column(db.Boolean, nullable=True)

    def __init__(self, id, domain_id, crt, descricao, regime_pis_cofins,
                 aliq_pis, aliq_cofins, contrib_ipi,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag=None)
        self.domain_id = domain_id
        self.crt = crt
        self.descricao = descricao
        self.regime_pis_cofins = regime_pis_cofins
        self.aliq_pis = aliq_pis
        self.aliq_cofins = aliq_cofins
        self.contrib_ipi = contrib_ipi

    @classmethod
    def individual(cls):
        return 'regimes_tributario'
