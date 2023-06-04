from pysnmp.hlapi.asyncore import *


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
def cbFun(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBindTable, cbCtx):

    if errorIndication:
        print(errorIndication)
        return

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBindTable[-1][int(errorIndex) - 1][0] or '?'))
        return

    else:
        for d, varBindRow in enumerate(varBindTable):
            for c, varBind in enumerate(varBindRow):
                print(d, c, ' = '.join([x.prettyPrint() for x in varBind]))

    print('end callback')
    return True


snmpEngine = SnmpEngine()

bulkCmd(snmpEngine,
		CommunityData('@c1sc0atl45t'),
		UdpTransportTarget(('cs1.dcg', 161)),
		ContextData(),
  		1,
		25,  
		ObjectType(ObjectIdentity('IP-MIB', 'ipAdEntAddr')),
    	ObjectType(ObjectIdentity('IP-MIB', 'ipAddrEntry')),
		cbFun=cbFun,
  		lexicographicMode=False)

print('dispatch')
snmpEngine.transportDispatcher.runDispatcher()