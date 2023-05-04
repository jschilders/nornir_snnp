from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir_snmp.plugins.tasks import snmp_bulk

from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cr1.dcg")

result = nr.run(task=snmp_bulk, oid=("JUNIPER-MIB", "jnxLEDTable"))
print_result(result)
