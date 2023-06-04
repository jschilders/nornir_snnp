from pysnmp.hlapi import *
from pysnmp.smi.view import MibViewController
from pysnmp.smi.builder import MibBuilder


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

	asn1Sources =  kwargs.pop('asn1Sources', False)
	mibSources =   kwargs.pop('mibSources', False)
	modNames =     kwargs.pop('modNames', False)
	resolveMib =   kwargs.pop('resolveMib', False)
	ignoreErrors = kwargs.pop('ignoreErrors', False)
 
	controller = MibViewController(MibBuilder())

	for varBind in varBinds:
		
		if asn1Sources:
			varBind.addAsn1MibSource(*asn1Sources)

		if mibSources:
			varBind.addMibSource(*mibSources)

		if modNames:
			varBind.loadMibs(*modNames)

		if resolveMib:
			varBind.resolveWithMib(controller, ignoreErrors=ignoreErrors)
 

	return varBinds

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
.getMibNode()
isFullyResolved()

addAsn1MibSource(*asn1Sources, **kwargs)	Adds path to a repository to search ASN.1 MIB files.
addMibSource(*mibSources)					Adds path to repository to search PySNMP MIB files.
loadMibs(*modNames)							Schedules search and load of given MIB modules.
resolveWithMib(mibViewController)			Perform MIB variable ID conversion.

Please refer to 
:py:class:`~pysmi.reader.localfile.FileReader`,
:py:class:`~pysmi.reader.httpclient.HttpReader` and
:py:class:`~pysmi.reader.ftpclient.FtpReader` classes for
in-depth information on ASN.1 MIB lookup.

FileReader(self, path, recursive=True, ignoreErrors=True)
def FtpReader(self, host, locationTemplate, timeout=5,
            ssl=False, port=21, user='anonymous',
            password='anonymous@'):
>>> mibViewController = varbinds.AbstractVarBinds.getMibViewController( engine )


ObjectType objects also support sequence protocol addressing objectIdentity as its 0-th element and objectSyntax as 1-st.
'''