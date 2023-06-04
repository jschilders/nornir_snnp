from pysnmp.error  import PySnmpError
requested_modNames = []

modName = lambda varBind: varBind[0]._ObjectIdentity__modName

def cbFun(snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBindsTable, cbContext):

	if errorIndication:
		raise PySnmpError(errorIndication)

	elif errorStatus:
		errorMessage = errorStatus.prettyPrint()
		errorLocation = varBindsTable[int(errorIndex) - 1][0] if errorIndex else '?'
		raise PySnmpError(f"{errorMessage} at {errorLocation}")

	global requested_modNames
	requested_modNames = requested_modNames or [ varBind.prettyPrint().split('::')[0] for varBind in varBindsTable[0] ]

	for varBinds in varBindsTable:
		stopflag = True
		for varBind, requested_modName in zip(varBinds, requested_modNames):
			if modName(varBind) == requested_modName:
				stopflag = False
				cbContext.append(varBind)
		if stopflag:
			break
	else:
		# Fetch next bactch
		return True

	# Fetched all results, clear table for next run
	requested_modNames = []
	

