def print_one(iterator):
	errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

	if errorIndication:
		print(errorIndication)

	elif errorStatus:
		print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

	else:
		for varBind in varBinds:
			print(' = '.join([x.prettyPrint() for x in varBind]))


def print_all(iterator):
	for errorIndication, errorStatus, errorIndex, varBinds in iterator:

		if errorIndication:
			print(errorIndication)
			break

		elif errorStatus:
			print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
			break

		else:
			for varBind in varBinds:
				print(' = '.join([x.prettyPrint() for x in varBind]))
			  

def get_all(iterator, format='dict'):
	result = []		  
	for errorIndication, errorStatus, errorIndex, varBinds in iterator:

		if errorIndication:
			result.append(errorIndication)

		elif errorStatus:
			result.append('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

		else:
			for varBind in varBinds:
				if format == 'tuple':
					result.append(tuple(x.prettyPrint() for x in varBind))
				elif format == 'dict':
					result.append({varBind[0].prettyPrint(): varBind[1].prettyPrint()})
				else:
					result.append(' = '.join([x.prettyPrint() for x in varBind]))
	return result		  
	
     
     
def get_all_dict(iterator):
	result = {}

	for errorIndication, errorStatus, errorIndex, varBinds in iterator:

		if errorIndication:
			
			return {'errorIndication': errorIndication}

		elif errorStatus:
			return {'errorStatus': f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}"}
				

		else:
			for varBind in varBinds:
				{varBind[0].prettyPrint(): varBind[1].prettyPrint()}
				
