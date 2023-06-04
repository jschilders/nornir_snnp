from pysnmp.hlapi import *
from nornir_snmp.plugins.connections import SNMP

test = SNMP()
test.open("cr1.eqam8", None, "@c1sc0atl45t")

iterator = test.connection.pysnmp_bulk("JUNIPER-MIB", "jnxLEDTable")
for i in iterator:
    print(i)

iterator = test.connection.pysnmp_bulk(
    nonRepeaters=0,
    maxRepetitions=50,
    varBind=ObjectType(ObjectIdentity("SNMPv2-MIB", "system")),
)
for i in iterator:
    print(i)
