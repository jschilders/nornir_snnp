from nornir_utils.plugins.functions import print_result
from nornir_snmp.plugins.tasks import snmp_bulk
from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cr1.dcg")
#
#result = nr.run(task=snmp_bulk, oid=("JUNIPER-MIB", "jnxLEDTable"))
#print_result(result)
#
#result = nr.run(task=snmp_bulk, oid=("SNMPv2-MIB", "system"), lexicographicMode=False)
#
#print_result(result)
#
result = nr.run(task=snmp_bulk, oids=[
        ("JUNIPER-MIB", "jnxLEDTable"),
        ("SNMPv2-MIB", "system")
    ]
)
print_result(result)



#result = nr.run(
#    task=snmp_bulk, 
#    oids=
#        [
#            ("SNMPv2-MIB", "sysDescr"),
#            ('SNMPv2-MIB', 'sysUpTime'),
#            ("JUNIPER-MIB", "jnxLEDTable")
#        ],
#    #nonRepeaters=2
#    )
#print_result(result)
