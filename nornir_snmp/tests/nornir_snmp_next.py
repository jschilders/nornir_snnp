from nornir_utils.plugins.functions import print_result
from nornir_snmp.plugins.tasks import snmp_next
from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cr1.dcg")

result = nr.run(task=snmp_next, oid=("SNMPv2-MIB", "system"))

print_result(result)

