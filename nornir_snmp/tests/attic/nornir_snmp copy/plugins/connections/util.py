from pysnmp.hlapi import *
from pysnmp.error import PySnmpError
from pysnmp.smi.view import MibViewController
from pysnmp.smi.builder import MibBuilder

# from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType


def copy_keys(source_dict, keys_to_copy):
    return {k: v for k, v in source_dict.items() if k in keys_to_copy}


def object_types(*args, **kwargs):
    objectTypes = []

    if args:
        objectTypes.append(ObjectType(object_identity(*args)))

    if varBind := kwargs.get("varBind", False):
        objectTypes.extend(varBind) if isinstance(
            varBind, list
        ) else objectTypes.append(varBind)

    if oid := kwargs.get("oid", False):
        objectTypes.append(ObjectType(object_identity(*oid)))

    if oids := kwargs.get("oids", False):
        for oid in oids:
            objectTypes.append(ObjectType(object_identity(*oid)))

    return objectTypes


def object_identity(*args, **kwargs):
    objectIdentity = ObjectIdentity(*args)

    if asn1Sources := kwargs.pop("asn1Sources", False):
        objectIdentity.addAsn1MibSource(*asn1Sources)

    if mibSources := kwargs.pop("mibSources", False):
        objectIdentity.addMibSource(*mibSources)

    if modNames := kwargs.pop("modNames", False):
        objectIdentity.loadMibs(*modNames)

    if kwargs.pop("resolveMib", False):
        controller = MibViewController(MibBuilder())
        ignoreErrors = kwargs.pop("ignoreErrors", False)
        objectIdentity.resolveWithMib(controller, ignoreErrors=ignoreErrors)

    return objectIdentity


def process_results(iterator):
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            raise PySnmpError(errorIndication)

        elif errorStatus:
            errorMessage = errorStatus.prettyPrint()
            errorLocation = varBinds[int(errorIndex) - 1][0] if errorIndex else "?"
            raise PySnmpError(f"{errorMessage} at {errorLocation}")

        yield from [varBind for varBind in varBinds]
