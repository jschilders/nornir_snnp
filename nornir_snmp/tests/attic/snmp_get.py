from pysnmp.hlapi import *
from nornir_snmp.plugins.connections import SNMP

test = SNMP()
test.open("cr1.eqam8", None, "@c1sc0atl45t", None, None)


#iterator = test.connection.pysnmp_get(
#    oid=ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0))
#)
#for i in iterator:
#    print("varBind", i)
#

iterator = test.connection.pysnmp_get(oid=("SNMPv2-MIB", "sysLocation", 0))
for i in iterator:
    print("args", i)


iterator = test.connection.pysnmp_get(
    oid=("SNMPv2-MIB", "sysDescr", 0),
)
for i in iterator:
    print("oid", i)


iterator = test.connection.pysnmp_get(
    oids=[
        ("SNMPv2-MIB", "sysDescr", 0),
        ("SNMPv2-MIB", "sysLocation", 0),
    ]
)
for i in iterator:
    print("oids", i)
