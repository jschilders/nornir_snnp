from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result
from nornir_snmp.plugins.tasks import snmp_get

from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cr1.dcg")

result = nr.run(
    task=snmp_get, 
    oid=("SNMPv2-MIB", "sysDescr", 0),
    #asn1Sources=['http://mibs.snmplabs.com/asn1/@mib@'],
    #mibSources=['/opt/nornir/nornir_snmp/nornir_snmp/pymibs'],
    resolveMib = True)
print_result(result)
