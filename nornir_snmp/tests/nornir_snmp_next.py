from nornir_utils.plugins.functions import print_result
from nornir_snmp.plugins.tasks import snmp_next
from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cr1.dcg")


result = nr.run(
    task=snmp_next, 
    oid=("JUNIPER-MIB", "jnxLEDTable"),
    addAsn1MibSource    = 'https://pysnmp.github.io/mibs/asn1/@mib@',  
    #payload        = 'rtrsdfs',
    lookupMib = True,
    lexicographicMode = True,
    ignoreNonIncreasingOid = True,
    maxRows = 19    ,
    addMibSource     = None,
    loadMibs       = None,
    resolveWithMib = None,
    ignoreErrors   = False,
    lajsdjhfalsdkjfskdj = 'asfsfgadfg'
)
print_result(result)


#nr = nornir_inventory().filter(hostname="cr1.dcg")

#result = nr.run(task=snmp_next, oid=("SNMPv2-MIB", "system"))
#print_result(result)

#result = nr.run(task=snmp_next, oids=[('IF-MIB', 'ifDescr')])
#print_result(result)

#result = nr.run(task=snmp_next, oid=('TCP-MIB'))
#print_result(result)



