from pysnmp.hlapi.asyncore import *
from rich import print

def cbFun(snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
    print(errorIndication, errorStatus, errorIndex, varBinds)

snmpEngine = SnmpEngine()

setCmd(snmpEngine,
       CommunityData('@c1sc0atl45t'),
       UdpTransportTarget(('cs1.dcg', 161)),
       ContextData(),
       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysContact', 0), 'info@snmplabs.com'),
       cbFun=cbFun)

snmpEngine.transportDispatcher.runDispatcher()