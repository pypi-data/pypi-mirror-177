from viggocore.database import db
from viggocore.subsystem.file.resource import File


class ArquivoIBPT(File, db.Model):

    attributes = ['sigla_uf']
    attributes += File.attributes

    id = db.Column(db.ForeignKey('file_infosys.id'), primary_key=True)
    sigla_uf = db.Column(db.CHAR(2), nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'arquivo_ibpt'}

    __tablename__ = 'arquivo_ibpt'

    def __init__(self, id, domain_id, name, sigla_uf,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, domain_id, name, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.domain_org_id = domain_id
        self.sigla_uf = sigla_uf

    @classmethod
    def individual(cls):
        return 'arquivo_ibpt'

    @classmethod
    def collection(cls):
        return 'arquivos_ibpt'
