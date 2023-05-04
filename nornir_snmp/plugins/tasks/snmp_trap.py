from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME

__all__ = ("snmp_trap")

def snmp_trap(task: Task, **kwargs) -> Result:
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
    #
    # Not implemented yet
    #
    results = None
    #results = device.pysnmp_trap(**kwargs)
    return Result(
        host=task.host,
        result=[ f"{name.prettyPrint()} = {value.prettyPrint()}" for name, value in results ]
    )