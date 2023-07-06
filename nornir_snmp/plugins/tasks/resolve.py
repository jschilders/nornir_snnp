
from typing import Union, Optional
from pysnmp.smi.view import MibViewController
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType, NotificationType
from pysnmp.proto.rfc1902 import ObjectIdentifier, ObjectName, ObjectSyntax


def str_or_list(_item: Union[str, list]) -> list:
    return [ _item ] if isinstance(_item, str) else _item


def copy_keys(_source_dict: dict, _keys_to_copy: list[str]):
    return {_key: _value for _key, _value in _source_dict.items() if _key in _keys_to_copy}


def make_object_identity(_oid, last=False, **options) -> ObjectIdentity:
    """
    _oid – initial MIB variable identity. Recognized variants:
      - single tuple of integers representing OID (1, 3, 6, 1, 2, 1, 1, 1, 0)
      - single str representing OID in dot-separated integers form '1.3.6.1.2.1.1.1.0'
      - single str representing MIB variable in dot-separated labels form 'iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0'
      - single str representing MIB name. First variable defined in MIB is assumed, unless last=True. 'SNMPv2-MIB'
      - pair of str representing MIB name and variable name 'SNMPv2-MIB', 'system'
      - pair of str representing MIB name and variable name followed by an arbitrary number of str and/or int values representing MIB variable instance identification. 'SNMPv2-MIB', 'sysDescr', 0

    kwargs – MIB resolution options(object):
      - whenever only MIB name is given, resolve into last variable defined in MIB if last=True. Otherwise resolves to first variable (default).
    
    Returns:
        ObjectIdentity

    """
    object_identity = ObjectIdentity(*str_or_list(_oid), last=last)
    
    enhance_object(object_identity, **options)
    return object_identity
    

def make_object_type(objectIdentity, objectSyntax=None, **options) -> ObjectType:
    """
    ObjectType(
        ObjectIdentity('SNMPv2-MIB', 'sysDescr'), 
        'Linux i386 box'
    )
    """
    if objectSyntax is None:
        object_type = ObjectType(make_object_identity(objectIdentity, **options))
    else:
        object_type = ObjectType(make_object_identity(objectIdentity, **options), objectSyntax)

    enhance_object(object_type, **options)
    return object_type


def make_notification_type(objectIdentity, instanceIndex, objects, **options) -> NotificationType:
    """
    NotificationType(ObjectIdentity('1.3.6.1.6.3.1.1.5.3'))

    NotificationType(
        ObjectIdentity('IP-MIB', 'linkDown'), 
        ObjectName('3.5')
    )

    Args:
        objectIdentity (ObjectIdentity) Class instance representing MIB notification type identification.

        instanceIndex (ObjectName)      Trailing part of MIB variables OID identification that represents concrete instance of a MIB variable. 
                                        When notification is prepared, instanceIndex is appended to each MIB variable 
                                        identification listed in NOTIFICATION-TYPE->OBJECTS clause.

        objects (dict)                  Dictionary-like object that may return values by OID key. 
                                        The objects dictionary is consulted when notification is being prepared. 
                                        OIDs are taken from MIB variables listed in NOTIFICATION-TYPE->OBJECTS with instanceIndex part appended.


    Returns:
        NotificationType


    addVarBinds(*varBinds)
        Appends variable-binding to notification.
        This method can be used to add custom variable-bindings to notification message
        in addition to MIB variables  specified in NOTIFICATION-TYPE->OBJECTS clause.

    NotificationType(ObjectIdentity('IP-MIB', 'linkDown')).addVarBinds(ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

    Parameters
        *varBinds (ObjectType) – One or more ObjectType class instances.

    Returns
        NotificationType


        
        
    """
    if instanceIndex:
        notification_type = ObjectType(make_object_identity(objectIdentity, **options), instanceIndex)
    else:
        notification_type = ObjectType(make_object_identity(objectIdentity, **options))

    if objects:
        notification_type.addVarBinds(objects)

    enhance_object(notification_type, **options)
    return notification_type


def enhance_object(object, 
                   addAsn1MibSource:list = None, 
                   addMibSource:list = None, 
                   loadMibs:list = None, 
                   resolveWithMib:MibViewController = None, 
                   ignoreErrors:bool = True ) -> object:
    """

    addAsn1MibSource(*asn1Sources, **kwargs)
        Adds path to a repository to search ASN.1 MIB files.

    addAsn1MibSource('https://mibs.pysnmp.com/asn1/@mib@')
    
    Parameters
        *asn1Sources – one or more URL in form of str identifying local or remote ASN.1 MIB repositories. 
        Path must include the @mib@ component which will be replaced with MIB module name at the time of search.
        Please refer to FileReader, HttpReader and FtpReader classes for in-depth information on ASN.1 MIB lookup.
        
    Returns
        ObjectIdentity

    ------

   addMibSource(*mibSources)
        Adds path to repository to search PySNMP MIB files.

    addMibSource('/opt/pysnmp/mibs', 'pysnmp_mibs')
    
    Parameters
        *mibSources – one or more paths to search or Python package names to import and search for PySNMP MIB modules.

    Returns
        ObjectIdentity
        
    ------

    loadMibs(*modNames)
        Schedules search and load of given MIB modules.

    loadMibs('IF-MIB', 'TCP-MIB')
    
    Parameters
        *modNames – one or more MIB module names to load up and use for MIB variables resolution purposes.

    Returns
        ObjectIdentity

    ------

    resolveWithMib(mibViewController, ignoreErrors=True)
        Perform MIB variable ID conversion.

    resolveWithMib(mibViewController)

    Parameters
        mibViewController (MibViewController) – class instance representing MIB browsing functionality.

    Returns
        ObjectIdentity

    ------
    """

    if addAsn1MibSource:
        object.addAsn1MibSource(*str_or_list(addAsn1MibSource))

    if addMibSource:
        object.addMibSource(*str_or_list(addMibSource))

    if loadMibs:
        object.loadMibs(*str_or_list(loadMibs))

    if resolveWithMib:
        object.resolveWithMib(resolveWithMib, ignoreErrors=ignoreErrors)

    return object


def resolve_mibs(oid=None, oids=None, payload=None, instance=None, objects=None, **kwargs):
#    oid:            Optional[Union[str, tuple]] =       None,      oid to resolve
#    oids:           Optional[list[Union[str, tuple]]] = None,      list of oids to resolve
#    payload:        Optional[str] = None,                          payload (objectSyntax) for 'set' operation
#    instance:       Optional(tuple) = None,                        instance index for notification or trap
#    objects:        Optional(dict) = None,                         extra objects for notification or trap

#    asn1Sources:    Optional[Union[str, list]] =        'https://pysnmp.github.io/mibs/asn1/@mib@',  
#    mibSources:     Optional[Union[str, list]] =        None,
#    modNames:       Optional[Union[str, list]] =        None,
#    resolveWithMib: Optional[MibViewController] =       None,
#    ignoreErrors:   Optional[bool] =                    False,
#    **kwargs        # catch undefined options
#

    options = copy_keys(kwargs, ['addAsn1MibSource', 'addMibSource', 'loadMibs', 'resolveWithMib', 'ignoreErrors'])

    if instance or objects:
        
        if oid is not None:
            return [make_notification_type(oid, instance, objects, **options)]
        if oids is not None:
            return [make_notification_type(oid, instance, objects, **options) for oid in oids]
    else:        
        if oid is not None:
            return [make_object_type(oid, payload, **options)]
        if oids is not None:
            return [make_object_type(oid, payload, **options) for oid in oids]

    return []


def mibviewcontroller():
    from pysnmp.entity.engine import SnmpEngine
    from pysnmp.hlapi.varbinds import AbstractVarBinds
    return AbstractVarBinds.getMibViewController(SnmpEngine())

