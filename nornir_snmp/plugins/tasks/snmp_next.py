from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME

__all__ = ("snmp_next")

def snmp_next(task: Task, **kwargs) -> Result:
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    results = device.pysnmp_next(**kwargs)
    return Result(
        host=task.host,
        result=[ f"{name.prettyPrint()} = {value.prettyPrint()}" for name, value in results ]
    )
