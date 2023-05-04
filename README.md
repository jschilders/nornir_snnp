# nornir_snmp

SNMP plugin for Nornir.


result = nornir.run(
    task=snmp_get, 
    oid=("SNMPv2-MIB", "sysDescr", 0),
)
print_result(result)
