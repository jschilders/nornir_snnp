from pysnmp.error import PySnmpError
from pysnmp.smi.view import MibViewController
from pysnmp.smi.builder import MibBuilder
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from enum import Enum
from typing import Any, Union, Iterator, List, Dict, Tuple

class State(Enum):
    ST_UNKNOWN = 0
    ST_DIRTY = 1
    ST_CLEAN = 2


def copy_keys(source_dict: Dict, keys_to_copy: List[Any]):
    return {k: v for k, v in source_dict.items() if k in keys_to_copy}


def generator_options(source_dict: Dict):
    options_keys = [
        'lookupMib',
        'lexicographicMode',
        'ignoreNonIncreasingOid',
        'maxRows',
        'maxRows'
    ]
    options = copy_keys(source_dict, options_keys)
    options.setdefault('lexicographicMode', False)
    return options


def varbinds_options(source_dict: Dict):
    options_keys = [
        'oid',
        'oids',
        'asn1Sources',
        'mibSources',
        'modNames',
        'resolveMib',
        'ignoreErrors'
    ]
    options = copy_keys(source_dict, options_keys)
    return options


def str_or_list(item: Union[str, List]) -> List:
    return [ item ] if isinstance(item, str) else item


def str_or_tuple(item: Union[str, Tuple]) -> List:
    return [ item ] if isinstance(item, str) else item


def ResolveMibs(
    oid:          Union[str, Tuple] = None,
    oids:         List[Union[str, Tuple]] = None,
    asn1Sources:  Union[str, List] = None,  
    mibSources:   Union[str, List] = None,
    modNames:     Union[str, List] = None,
    resolveMib:   bool = True,
    ignoreErrors: bool = False,
    **kwargs      # catch undefined options
) -> list[ObjectType]:
    """
    Create a list of ObjectType object instances holding MIB information

    Args:
        oid (tuple or str):
            single MIB variable identity. See below for formats
        oids (list[oid]):
            list of MIB variable identities. See below for formats
        asn1Sources (str or list[str]) :
            one or more strings identifying URLs to local or remote ASN.1 MIB repositories. 
            Supported are 'http://', 'ftp://', and 'file://' URLs. 
            Use *@mib@* as placeholder which will be replaced with MIB module name.
        mibSources (str or list[str]) :
            one or more paths to search or Python package names to importand search for PySNMP MIB modules.
        modNames (str or list[str]) :
            one or more MIB module names to load up and use for MIB
            variables resolution purposes.
        resolveWithMib (bool, default=True):
            Perform MIB variable ID conversion.
            Options:
                ignoreErrors (bool, default=True)

    Recognized variants for MIB variable identity:
        - a tuple of integers representing OID.
        - a str representing OID in dot-separated integers form.
        - a str representing MIB variable in dot-separated labels form.
        - a str representing MIB name. First variable defined in MIB is assumed.
        - a tuple of str representing MIB name and variable name.
        - a tuple of str representing MIB name and variable name, followed by any number of indexes.
        - a predefined or configured ObjectType instance object.

    Returns:
        list[ObjectType]: List with resolved ObjectType object instances
    """
    def make_object_identity(oid: Union[str, Tuple]) -> ObjectIdentity:

        object_identity = ObjectIdentity(*str_or_tuple(oid))

        if asn1Sources:
            object_identity.addAsn1MibSource(*str_or_list(asn1Sources))
        if mibSources:
            object_identity.addMibSource(*str_or_list(mibSources))
        if modNames:
            object_identity.loadMibs(*str_or_list(modNames))
        if resolveMib:
            object_identity.resolveWithMib(controller, ignoreErrors=ignoreErrors)

        return object_identity


    def make_object_type(oid: Union[str, Tuple]) -> ObjectType:

        if isinstance(oid, ObjectType):
            return oid
        else:
            return ObjectType(make_object_identity(oid))


    def resolve_object(oid: Union[str, Tuple]) -> ObjectType:

        if resolveMib:
            return make_object_type(oid).resolveWithMib(controller, ignoreErrors=ignoreErrors)
        else:
            return make_object_type(oid)


    controller = MibViewController(MibBuilder())
    
    if oid:
        return [resolve_object(oid)]
    if oids:
        return [resolve_object(oid) for oid in oids]

    return []


def process_results(iterator: Iterator) -> ObjectType:

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            raise PySnmpError(errorIndication)
        elif errorStatus:
            errorMessage = errorStatus.prettyPrint()
            errorLocation = varBinds[int(errorIndex) - 1][0] if errorIndex else "?"
            raise PySnmpError(f"{errorMessage} at {errorLocation}")

        yield from [varBind for varBind in varBinds]
