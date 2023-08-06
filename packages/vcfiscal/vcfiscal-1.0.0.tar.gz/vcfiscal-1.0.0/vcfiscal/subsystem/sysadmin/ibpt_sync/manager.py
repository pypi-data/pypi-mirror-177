from viggocore.common.subsystem import manager, operation
from vcfiscal.subsystem.parametrizacao.ibpt.resource import IBPT
from vcfiscal.subsystem.sysadmin.ibpt_sync.resource import Status, IBPTSync


class VerifySync(operation.Count):

    def pre(self, session, **kwargs):
        self.chave = kwargs.get('chave', None)
        self.versao = kwargs.get('versao', None)
        self.sigla_uf = kwargs.get('sigla_uf', None)
        return super().pre()

    def do(self, session, **kwargs):
        query = session.query(IBPTSync). \
            join(IBPT, IBPTSync.ibpt_id == IBPT.id). \
            filter(IBPT.chave == self.chave). \
            filter(IBPT.versao == self.versao). \
            filter(IBPTSync.sigla_uf == self.sigla_uf). \
            filter(IBPTSync.status == Status.Sucesso). \
            distinct()
        result = query.count()

        return result


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.verify_sync = VerifySync(self)
