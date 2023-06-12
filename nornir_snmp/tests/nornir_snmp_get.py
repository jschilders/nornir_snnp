from nornir_utils.plugins.functions import print_result
from nornir_snmp.plugins.tasks import snmp_get
from nornir_snmp.tests.init_nornir import nornir_inventory


nr = nornir_inventory().filter(hostname="cs1.dcg")

result = nr.run(
    task=snmp_get, 
    oids=[
        ("SNMPv2-MIB", "sysDescr", 0),
        ('SNMPv2-MIB', 'sysUpTime', 0)
    ]
)
print_result(result)

nr = nornir_inventory().filter(hostname="cr1.dcg")


result = nr.run(
    task=snmp_get, 
    oid=('SNMPv2-MIB', 'sysUpTime', 0),
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

