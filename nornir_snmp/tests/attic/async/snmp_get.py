from pysnmp.hlapi.asyncore import *
from rich import print

def cbFun(snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
    print(errorIndication, errorStatus, errorIndex, varBinds)

snmpEngine = SnmpEngine()

getCmd(snmpEngine,
       CommunityData('@c1sc0atl45t'),
       UdpTransportTarget(('cs1.dcg', 161)),
       ContextData(),
       ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
       cbFun=cbFun)

snmpEngine.transportDispatcher.runDispatcher()