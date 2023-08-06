from viggocore.database import db
from viggocore.subsystem import domain


class DomainFiscal(domain.resource.Domain, db.Model):

    attributes = ['nfce_csc_id', 'nfce_csc',
                  'nfce_csc_id_homolog', 'nfce_csc_homolog']
    attributes += domain.resource.Domain.attributes

    id = db.Column(db.ForeignKey('domain.id'), primary_key=True)
    nfce_csc_id = db.Column(db.String(6), nullable=False)
    nfce_csc = db.Column(db.String(36), nullable=False)
    nfce_csc_id_homolog = db.Column(db.String(6), nullable=False)
    nfce_csc_homolog = db.Column(db.String(36), nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'domain_fiscal'}

    def __init__(self, id, name, cnpj, nfce_csc_id, nfce_csc,
                 nfce_csc_id_homolog, nfce_csc_homolog,
                 parent_id=None, active=True, created_at=None,
                 created_by=None, updated_at=None, updated_by=None, tag=None):
        super().__init__(id, name, parent_id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.nfce_csc_id = nfce_csc_id
        self.nfce_csc = nfce_csc
        self.nfce_csc_id_homolog = nfce_csc_id_homolog
        self.nfce_csc_homolog = nfce_csc_homolog

    @classmethod
    def individual(cls):
        return 'domain_fiscal'
