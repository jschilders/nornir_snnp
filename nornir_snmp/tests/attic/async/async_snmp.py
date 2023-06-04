from pysnmp.hlapi.asyncore import *


def cbFun(snmpEngine, sendRequestHandle, errorIndication,
		  errorStatus, errorIndex, varBindTable, cbCtx):

	authData, transportTarget = cbCtx

	print('%s via %s' % (authData, transportTarget))

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
		
		if not isEndOfMib(varBindTable[-1]):
			print('return callback')
			return True

		print('end callback')
		#return True


snmpEngine = SnmpEngine()

bulkCmd(snmpEngine,
		CommunityData('@c1sc0atl45t'),
		UdpTransportTarget(('cs1.dcg', 161)),
		ContextData(),
  		0,
		50,  
		#ObjectType(ObjectIdentity('IP-MIB', 'ipAdEntAddr')),
		#ObjectType(ObjectIdentity('IP-MIB', 'ipAddrEntry')),
		ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),
		cbFun=cbFun,
		cbCtx=('authData', 'transportTarget'),
  		lexicographicMode=False)

print('dispatch')
snmpEngine.transportDispatcher.runDispatcher()