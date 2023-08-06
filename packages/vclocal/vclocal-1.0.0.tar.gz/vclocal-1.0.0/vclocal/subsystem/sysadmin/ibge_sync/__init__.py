from viggocore.common import subsystem
from vclocal.subsystem.sysadmin.ibge_sync \
  import resource, manager

subsystem = subsystem.Subsystem(resource=resource.IbgeSync,
                                manager=manager.Manager)
