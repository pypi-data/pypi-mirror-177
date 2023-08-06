from viggocore.common import subsystem
from vcfiscal.subsystem.sysadmin.ibpt_sync import resource, manager

subsystem = subsystem.Subsystem(resource=resource.IBPTSync,
                                manager=manager.Manager)
