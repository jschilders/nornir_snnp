
from typing import Union, Optional
from pysnmp.smi.view import MibViewController
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType


def str_or_list(item: Union[str, list]) -> list:
    return [ item ] if isinstance(item, str) else item


def ResolveMibs(
    oid:            Optional[Union[str, tuple]] =       None,
    oids:           Optional[list[Union[str, tuple]]] = None,
    payload:        Optional[str] = None,
    
    asn1Sources:    Optional[Union[str, list]] =        'https://pysnmp.github.io/mibs/asn1/@mib@',  
    mibSources:     Optional[Union[str, list]] =        None,
    modNames:       Optional[Union[str, list]] =        None,
    resolveWithMib: Optional[MibViewController] =       None,
    ignoreErrors:   Optional[bool] =                    False,
    **kwargs        # catch undefined options
) -> list[ObjectType]:
    """
    Create a list of ObjectType object instances holding MIB information

    Args:
        oid (tuple or str):
            single MIB variable identity. See below for formats
        oids (list[oid]):
            list of MIB variable identities. See below for formats
            
        Recognized variants for MIB variable identity:
            - a tuple of integers representing OID.
            - a str representing OID in dot-separated integers form.
            - a str representing MIB variable in dot-separated labels form.
            - a str representing MIB name. First variable defined in MIB is assumed.
            - a tuple of str representing MIB name and variable name.
            - a tuple of str representing MIB name and variable name, followed by any number of indexes.
            - a predefined or configured ObjectType instance object.

        asn1Sources (str or list[str]) :
            one or more strings identifying URLs to local or remote ASN.1 MIB repositories. 
            Supported are 'http://', 'ftp://', and 'file://' URLs. 
            Use *@mib@* as placeholder which will be replaced with MIB module name.
            Example: 'https://pysnmp.github.io/mibs/asn1/@mib@'
        mibSources (str or list[str]) :
            one or more paths to search or Python package names to importand search for PySNMP MIB modules.
        modNames (str or list[str]) :
            one or more MIB module names to load up and use for MIB
            variables resolution purposes.
        resolveWithMib (MibViewController):
            Perform MIB variable ID conversion to fully initialize returned object

            Parameters: initialized MibViewController instance.
            Options:
                ignoreErrors (bool, default=True)

    Returns:
        list[ObjectType]: List with resolved ObjectType object instances
    """
    def make_object_identity(oid: Union[str, tuple]) -> ObjectIdentity:

        object_identity = ObjectIdentity(*str_or_list(oid))

        if asn1Sources:
            object_identity.addAsn1MibSource(*str_or_list(asn1Sources))
        if mibSources:
            object_identity.addMibSource(*str_or_list(mibSources))
        if modNames:
            object_identity.loadMibs(*str_or_list(modNames))
        if resolveWithMib:
            object_identity.resolveWithMib(resolveWithMib, ignoreErrors=ignoreErrors)

        return object_identity


    def make_object_type(oid: Union[str, tuple]) -> ObjectType:

        if payload:
            object_type = ObjectType(make_object_identity(oid), payload)
        else:
            object_type = ObjectType(make_object_identity(oid))

        if asn1Sources:
            object_type.addAsn1MibSource(*str_or_list(asn1Sources))
        if mibSources:
            object_type.addMibSource(*str_or_list(mibSources))
        if modNames:
            object_type.loadMibs(*str_or_list(modNames))
        if resolveWithMib:
            object_type.resolveWithMib(resolveWithMib, ignoreErrors=ignoreErrors)

        return object_type

    if oid is not None:
        return [make_object_type(oid)]
    if oids is not None:
        return [make_object_type(oid) for oid in oids]

    return []

