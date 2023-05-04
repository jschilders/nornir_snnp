from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME

__all__ = ("snmp_bulk")

def snmp_bulk(task: Task, **kwargs) -> Result:
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    kwargs.setdefault('lexicographicMode', False)
    results = device.pysnmp_bulk(**kwargs)
    return Result(
        host=task.host,
        result=[ f"{name.prettyPrint()} = {value.prettyPrint()}" for name, value in results ]
    )
