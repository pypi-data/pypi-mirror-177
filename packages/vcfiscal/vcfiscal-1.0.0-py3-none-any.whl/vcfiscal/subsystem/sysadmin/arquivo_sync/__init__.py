from viggocore.common import subsystem
from vcfiscal.subsystem.sysadmin.arquivo_sync import manager, resource, \
    controller

subsystem = subsystem.Subsystem(manager=manager.Manager,
                                controller=controller.Controller,
                                resource=resource.ArquivoSync)
