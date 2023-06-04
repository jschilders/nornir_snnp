from pysnmp.hlapi import *
from nornir_snmp.plugins.connections import SNMP

test = SNMP()
test.open("cr1.eqam8", None, "@c1sc0atl45t")

iterator = test.connection.pysnmp_next("JUNIPER-MIB", "jnxLEDTable")
for i in iterator:
    print(i)

iterator = test.connection.pysnmp_next(
    varBind=ObjectType(ObjectIdentity("SNMPv2-MIB", "system"))
)
for i in iterator:
    print(i)
