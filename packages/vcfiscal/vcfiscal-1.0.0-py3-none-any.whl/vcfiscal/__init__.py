import os
import viggocore
import vclocal

from flask_cors import CORS

from viggocore.system import System

from vcfiscal.subsystem.sysadmin import ibpt_sync, arquivo_ibpt
from vcfiscal.subsystem.parametrizacao \
    import domain_fiscal, ibpt, cfop, cest, ncm, \
    regime_tributario, operacao_fiscal, ibpt_ncm, ncm_cest
from vcfiscal.resources import SYSADMIN_EXCLUSIVE_POLICIES, \
    SYSADMIN_RESOURCES, USER_RESOURCES


system = System('vcfiscal',
                [domain_fiscal.subsystem, ibpt.subsystem, ibpt_sync.subsystem,
                 cfop.subsystem, cest.subsystem, ncm.subsystem,
                 regime_tributario.subsystem, operacao_fiscal.subsystem,
                 ibpt_ncm.subsystem, arquivo_ibpt.subsystem, ncm_cest.subsystem
                 ],
                USER_RESOURCES,
                SYSADMIN_RESOURCES,
                SYSADMIN_EXCLUSIVE_POLICIES)


class SystemFlask(viggocore.SystemFlask):

    def __init__(self):
        super().__init__(system, vclocal.system)
        #     # VCLocal
        #     uf.subsytem,

        #     # VCFiscal
        #     domain_fiscal, ibpt.subsystem, ibpt_sync.subsystem,
        #     cfop.subsystem, cest.subsystem, ncm.subsystem,
        #     regime_tributario.subsystem, operacao_fiscal.subsystem,
        #     ibpt_ncm.subsystem, arquivo_ibpt.subsystem
        # )

    def configure(self):
        origins_urls = os.environ.get('ORIGINS_URLS', '*')
        CORS(self, resources={r'/*': {'origins': origins_urls}})

        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        vcfiscal_database_uri = os.getenv('VCFISCAL_DATABASE_URI', None)
        if vcfiscal_database_uri is None:
            raise Exception('VCFISCAL_DATABASE_URI not defined in enviroment.')
        else:
            # URL os enviroment example for MySQL
            # export VCFISCAL_DATABASE_URI=
            # mysql+pymysql://root:mysql@localhost:3306/vcfiscal
            self.config['SQLALCHEMY_DATABASE_URI'] = vcfiscal_database_uri
