import enum

from sqlalchemy import UniqueConstraint, Enum, orm

from viggocore.common.subsystem import entity
from viggocore.database import db


class DESTINATARIO(enum.Enum):
    CONTRIBUINTE = 0
    NAO_CONTRIBUINTE = 1
    CONTRIBUINTE_ISENTO = 2


# TODO melhorar a sequencia em codigo
class OperacaoFiscal(entity.Entity, db.Model):
    attributes = ["regime_tributario_id", "ncm_id", "cfop_id", "codigo",
                  "descricao", "destinatario", "origem", "cst_icms",
                  "csosn_icms", "cest", "mva", "cst_pis", "aliq_ipi", "fcp",
                  "aliq_icms_interna", "aliq_icms_externa", "diferimento",
                  "aliq_pis", "cst_cofins", "aliq_cofins", "texto_legal"]
    attributes += entity.Entity.attributes

    regime_tributario_id = db.Column(
        db.CHAR(32), db.ForeignKey('regime_tributario.id'), nullable=False)
    regime_tributario = orm.relationship(
        "RegimeTributario",
        backref=orm.backref('operacao_fiscal_regime_tributario'))
    ncm_id = db.Column(db.CHAR(32), db.ForeignKey('ncm.id'), nullable=False)
    ncm = orm.relationship("NCM", backref=orm.backref('operacao_fiscal_ncm'))
    cfop_id = db.Column(db.CHAR(32), db.ForeignKey('cfop.id'), nullable=False)
    cfop = orm.relationship("CFOP",
                            backref=orm.backref('operacao_fiscal_cfop'))
    codigo = db.Column(db.Numeric(6), db.Sequence('operacao_fiscal_codigo_sq'),
                       nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    destinatario = db.Column(Enum(DESTINATARIO), nullable=True)
    origem = db.Column(db.Numeric(1), nullable=False)
    cst_icms = db.Column(db.CHAR(2), nullable=True)
    csosn_icms = db.Column(db.CHAR(3), nullable=True)
    cest = db.Column(db.CHAR(7), nullable=True)
    aliq_icms_interna = db.Column(db.Numeric(5, 2), nullable=False)
    aliq_icms_externa = db.Column(db.Numeric(5, 2), nullable=False)
    mva = db.Column(db.Numeric(5, 2), nullable=True)
    diferimento = db.Column(db.Numeric(5, 2), nullable=True)
    fcp = db.Column(db.Numeric(5, 2), nullable=True)
    aliq_ipi = db.Column(db.Numeric(5, 2), nullable=True)
    cst_pis = db.Column(db.CHAR(2), nullable=False)
    aliq_pis = db.Column(db.Numeric(6, 2), nullable=True)
    cst_cofins = db.Column(db.CHAR(2), nullable=False)
    aliq_cofins = db.Column(db.Numeric(6, 2), nullable=True)
    texto_legal = db.Column(db.String(200), nullable=True)

    __table_args__ = (
        UniqueConstraint('regime_tributario_id', 'codigo',
                         name='operacao_fiscal_reg_trib_id_codigo_uk'),
        UniqueConstraint('regime_tributario_id', 'ncm_id', 'cfop_id',
                         name='operacao_fiscal_reg_trib_id_ncm_id_cfop_id_uk'),
    )

    def __init__(self, id, regime_tributario_id, ncm_id, cfop_id, codigo,
                 descricao, origem, aliq_icms_interna, aliq_icms_externa,
                 cst_pis, cst_cofins, destinatario=None, cst_icms=None,
                 csosn_icms=None, cest=None, mva=None, diferimento=None,
                 fcp=None, aliq_ipi=None, aliq_pis=None, aliq_cofins=None,
                 texto_legal=None, active=True, created_at=None,
                 created_by=None, updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.regime_tributario_id = regime_tributario_id
        self.ncm_id = ncm_id
        self.cfop_id = cfop_id
        self.codigo = codigo
        self.descricao = descricao
        self.origem = origem
        self.aliq_icms_interna = aliq_icms_interna
        self.aliq_icms_externa = aliq_icms_externa
        self.cst_pis = cst_pis
        self.cst_cofins = cst_cofins
        self.destinatario = destinatario
        self.cst_icms = cst_icms
        self.csosn_icms = csosn_icms
        self.cest = cest
        self.mva = mva
        self.diferimento = diferimento
        self.fcp = fcp
        self.aliq_ipi = aliq_ipi
        self.aliq_pis = aliq_pis
        self.aliq_cofins = aliq_cofins
        self.texto_legal = texto_legal

    @classmethod
    def individual(cls):
        return "operacao_fiscal"

    @classmethod
    def collection(cls):
        return "operacao_fiscais"
