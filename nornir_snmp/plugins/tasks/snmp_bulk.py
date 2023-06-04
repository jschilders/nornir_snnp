from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME
from nornir_snmp.plugins.tasks.resolve  import ResolveMibs
from nornir_snmp.plugins.tasks.results  import get_results


def snmp_bulk(task: Task, **options) -> Result:

    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    oidlist = ResolveMibs(**options)

    iterator = device.pysnmp_bulk(*oidlist, **options)

    results = get_results(iterator)

    return Result(
        host=task.host,
        result=results
    )

