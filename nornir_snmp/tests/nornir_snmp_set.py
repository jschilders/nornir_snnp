from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir_snmp.plugins.tasks import snmp_get

from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory()

filter(hostname="cs1.dcg")

result = nr.run(
    task=snmp_get, 
    oid=("SNMPv2-MIB", "sysDescr", 0),
    payload = 'test'
)
print_result(result)

