from pysnmp.hlapi import *
from iterate import print_all, get_all
from nornir_snmp.plugins.connections import SNMP


from pysnmp.entity.engine import SnmpEngine
from pysnmp.entity import config
from pysnmp.smi.view import MibViewController
from pysnmp.smi.compiler import addMibCompiler
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType

snmpEngine = SnmpEngine()

addMibCompiler(snmpEngine.getMibBuilder())
mibViewController = MibViewController(snmpEngine.getMibBuilder())



test = SNMP()
test.open('cr1.eqam8', None, '@c1sc0atl45t')



addMibCompiler(test.connection[0].getMibBuilder())
mibViewController = MibViewController(test.connection[0].getMibBuilder())


# JUNIPER-MIB::jnxOperatingTable
# JUNIPER-MIB::jnxOperatingDescr


iterator = getCmd(
    *test.connection,
    ObjectType(ObjectIdentity('1.3.6.1.4.1.2636.3.1.13.1.5')),
)


#result = get_all(iterator)
result = list(iterator)

print(result)


#>>> 

# getCmd(snmpEngine, authData, transportTarget, contextData, *varBinds, **options )