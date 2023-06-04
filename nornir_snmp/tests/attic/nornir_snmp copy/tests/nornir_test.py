# Initializing objects for later use
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir_snmp.plugins.tasks import snmp_get

nr = InitNornir(
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml",
        },
    },
)

# filtering objects to simplify output
nr = nr.filter(hostname="cr1.dcg")


result = nr.run(snmp_get, "aaa", oid=("SNMPv2-MIB", "sysDescr", 0))
print_result(result)
