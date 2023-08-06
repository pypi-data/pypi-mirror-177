from viggocore.common import subsystem
from vcfiscal.subsystem.sysadmin.arquivo_ibpt import manager, resource, \
    controller

subsystem = subsystem.Subsystem(manager=manager.Manager,
                                controller=controller.Controller,
                                resource=resource.ArquivoIBPT)
