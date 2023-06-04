from pysnmp.hlapi import *
from functools import wraps
from pysnmp.error  import PySnmpError
from pysnmp.smi.view import MibViewController
from pysnmp.smi.builder import MibBuilder

def copy_keys(source_dict, keys_to_copy):
	return {k: v for k, v in source_dict.items() if k in keys_to_copy}


def mydecorator(wrapped_function):

	@wraps(wrapped_function)
	def wrapper(*args, **kwargs):
		kwargs['varBind'] = make_varBinds(*args[1:], **kwargs)
		iterator = wrapped_function(*args, **kwargs)
		yield from process_results(iterator)

	return wrapper


def make_varBinds(*args, **kwargs):

	varBinds = []

	if oids:= kwargs.get('oids', None):
		for oid in oids:
			varBinds.append(ObjectType(ObjectIdentity(*oid)))

	if oid:= kwargs.get('oid', None):
		varBinds.append(ObjectType(ObjectIdentity(*oid)))

	if varBind:= kwargs.get('varBind', None):
		if isinstance(varBind, list):
			varBinds.extend(varBind)
		else:
			varBinds.append(varBind)

	if args:
		varBinds.append(ObjectType(ObjectIdentity(*args)))
  
	# Enhance objects
 
#	for varBind in varBinds:
#		#
#		varBind.addAsn1MibSource(*asn1Sources, **kwargs)
#		#
#		varBind.addMibSource(*mibSources)
#  		#
#		varBind.loadMibs(*modNames)
#  		#
#		m = MibViewController(MibBuilder())
#		varBind.resolveWithMib(m, ignoreErrors=True)
 

	return varBinds


def process_results(iterator):
  
	for errorIndication, errorStatus, errorIndex, varBinds in iterator:

		if errorIndication:
			raise PySnmpError(errorIndication)

		elif errorStatus:
			errorMessage = errorStatus.prettyPrint()
			errorLocation = varBinds[int(errorIndex) - 1][0] if errorIndex else '?'
			raise PySnmpError(f"{errorMessage} at {errorLocation}")

		yield from  ((varBind[0].prettyPrint(), varBind[1].prettyPrint()) for varBind in varBinds)


'''
class pysnmp.smi.rfc1902.ObjectIdentity(*args, **kwargs)


Parameters:	
args – initial MIB variable identity. Recognized variants:

single tuple or integers representing OID
single str representing OID in dot-separated integers form
single str representing MIB variable in dot-separated labels form
single str representing MIB name. First variable defined in MIB is assumed.
pair of str representing MIB name and variable name
pair of str representing MIB name and variable name followed by an arbitrary number of str and/or int values representing MIB variable instance identification.

Other Parameters:
 	
kwargs – MIB resolution options(object):

whenever only MIB name is given, resolve into last variable defined in MIB if last=True. Otherwise resolves to first variable (default).
Notes

Actual conversion between MIB variable representation formats occurs upon resolveWithMib() invocation.

.getMibSymbol()	-> 	('SNMPv2-MIB', 'sysDescr', (0,))
.getOid()		-> 	ObjectName('1.3.6.1.2.1.1.1.0')
.getLabel()		->	('iso', 'org', 'dod', 'internet', 'mgmt', 'mib-2', 'system', 'sysDescr')

addAsn1MibSource(*asn1Sources, **kwargs)	Adds path to a repository to search ASN.1 MIB files. Please refer to FileReader, HttpReader and FtpReader classes for in-depth information on ASN.1 MIB lookup.
addMibSource(*mibSources)					Adds path to repository to search PySNMP MIB files.
loadMibs(*modNames)							Schedules search and load of given MIB modules.
resolveWithMib(mibViewController)			Perform MIB variable ID conversion.

		
>>> mibViewController = varbinds.AbstractVarBinds.getMibViewController( engine )


ObjectType objects also support sequence protocol addressing objectIdentity as its 0-th element and objectSyntax as 1-st.
'''