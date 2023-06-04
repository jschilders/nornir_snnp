from pysnmp.hlapi.asyncore import *
from cbFun import cbFun

cbContext = []

snmpEngine = SnmpEngine()

bulkCmd(snmpEngine,
		CommunityData('@c1sc0atl45t'),
		UdpTransportTarget(('cs1.dcg', 161)),
		ContextData(),
		0, 5,
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')),
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysLocation')),
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName')),
		cbFun=cbFun,
  		cbCtx=cbContext)

snmpEngine.transportDispatcher.runDispatcher()

for i in cbContext:
    print(i)
    
cbCtx2 = []

bulkCmd(snmpEngine,
		CommunityData('@c1sc0atl45t'),
		UdpTransportTarget(('cs1.dcg', 161)),
		ContextData(),
		0, 5,
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr')),
		cbFun=cbFun,
  		cbCtx=cbCtx2)

snmpEngine.transportDispatcher.runDispatcher()

