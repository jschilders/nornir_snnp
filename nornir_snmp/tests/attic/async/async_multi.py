from pysnmp.hlapi.asyncore import *

# List of targets in the following format:
# ((authData, transportTarget, varNames), ...)
targets = (
#    # 1-st target (SNMPv1 over IPv4/UDP)
#    (CommunityData('@c1sc0atl45t'),
#		UdpTransportTarget(('cs1.dcg', 161)),
#     (ObjectType(ObjectIdentity('1.3.6.1.2.1')),
#      ObjectType(ObjectIdentity('1.3.6.1.3.1')))),
#
#    # 2-nd target (SNMPv2c over IPv4/UDP)
#    (CommunityData('@c1sc0atl45t'),
#		UdpTransportTarget(('cs1.dcg', 161)),
#     (ObjectType(ObjectIdentity('1.3.6.1.4.1')),)),
#
    # 3-nd target (SNMPv3 over IPv4/UDP)
#  @ (CommunityData('@c1sc0atl45t'),
#		UdpTransportTarget(('cs1.dcg', 161)),
#    (ObjectType(ObjectIdentity('SNMPv2-MIB', 'system')),)),

	# 4-th target (SNMPv3 over IPv6/UDP)
	(
		CommunityData('@c1sc0atl45t'),
		UdpTransportTarget(('cs1.dcg', 161)),
		(ObjectType(ObjectIdentity('IF-MIB', 'ifTable')),)
	),

	# N-th target
	# ...
)


# Wait for responses or errors, submit GETNEXT requests for further OIDs
# noinspection PyUnusedLocal,PyUnusedLocal
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
	  
	  
	  
		for varBindRow in varBindTable:
			for varBind in varBindRow:
				print(' = '.join([x.prettyPrint() for x in varBind]))

		return True  # continue table retrieval


snmpEngine = SnmpEngine()

# Submit initial GETNEXT requests and wait for responses
for authData, transportTarget, varBinds in targets:
	nextCmd(snmpEngine, authData, transportTarget, ContextData(),
			*varBinds, cbFun=cbFun, cbCtx=(authData, transportTarget))

snmpEngine.transportDispatcher.runDispatcher()