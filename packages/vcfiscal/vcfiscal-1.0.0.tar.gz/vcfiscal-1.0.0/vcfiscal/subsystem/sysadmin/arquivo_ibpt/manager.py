from viggocore.subsystem.file import manager
from vcfiscal.subsystem.sysadmin.arquivo_ibpt import tasks


class Create(manager.Create):

    def pre(self, session, **kwargs):
        self.sigla_uf = kwargs.get('sigla_uf', None)
        return super().pre(session=session, **kwargs)

    def post(self):
        tasks.process_arquivo_ibpt(self.sigla_uf,
                                   self.entity.filename,
                                   self.upload_folder,
                                   self.user_id)


class Manager(manager.Manager):

    ALLOWED_EXTENSIONS = ['csv']

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
