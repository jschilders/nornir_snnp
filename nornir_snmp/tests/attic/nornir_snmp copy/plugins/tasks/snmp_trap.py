from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME

# TODO: NOT TESTED


def snmp_trap(task: Task, *args, **kwargs) -> Result:
    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    results = device.pysnmp_trap(*args, **kwargs)

    return Result(
        host=task.host,
        result=[
            name.prettyPrint + " = " + value.prettyPrint for name, value in results
        ],
    )
