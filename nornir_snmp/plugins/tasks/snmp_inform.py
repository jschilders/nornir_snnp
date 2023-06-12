from nornir.core.task import Result, Task
from nornir_snmp.plugins.connections import CONNECTION_NAME
from nornir_snmp.plugins.tasks.resolve  import resolve_mibs
from nornir_snmp.plugins.tasks.results  import get_results


def snmp_inform(task: Task, **options) -> Result:

    device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)

    oids = resolve_mibs(**options)

    iterator = device.pysnmp_inform(*oids, **options)

    results = get_results(iterator)
   
    return Result(
        host=task.host,
        result=results
    )

