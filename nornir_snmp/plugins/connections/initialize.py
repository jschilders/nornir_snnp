from typing import Any, Optional, Union

from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.auth import CommunityData, UsmUserData
from pysnmp.hlapi.asyncore.transport import UnixTransportTarget, Udp6TransportTarget, UdpTransportTarget
from pysnmp.hlapi.context import ContextData

def copy_keys(source_dict: dict, keys_to_copy: list[str]):
    return {k: v for k, v in source_dict.items() if k in keys_to_copy}


def engine_object(parameters) -> SnmpEngine:
    """
    Return class instance representing SNMP engine

    Parameters:
        snmpEngineID (str) :
            Optional engine ID

    Returns:
        SnmpEngine (:py:class:`~pysnmp.hlapi.SnmpEngine`): Class instance representing SNMP engine
    """
    snmp_engine_params = copy_keys(parameters,
        [
            'snmpEngineID'
        ]
    )

    return SnmpEngine(**snmp_engine_params)


def authentication_object(parameters) -> Union[CommunityData, UsmUserData]:
    """
    Return class instance representing SNMP credentials.

    Parameters:
        snmp_protocol (str):
            SNMP Protocol to use. 'V1', 'V2c' or 'V3' suggested, but any string containing a 1, 2 or 3 will do.

    Parameters for SNMP V1 or V2c:
        communityIndex (str) :
            Unique index value of a row in snmpCommunityTable.
        communityName (str) :
            SNMP v1/v2c community string
        contextEngineId (str) :
            Indicates the location of the context in which management information is accessed when using the community string specified by the above communityName.
        contextName (str) :
            The context in which management information is accessed when using the above communityName.
        tag (str) :
            Arbitrary string that specifies a set of transport endpoints.

    Parameters for SNMP V3:
        userName (str):
            A human readable string representing the name of the SNMP USM user
        authKey (str):
            Initial value of the secret authentication key. If not set, 'usmNoAuthProtocol' is implied.
        privKey (str):
            Initial value of the secret encryption key.  If not set, 'usmNoPrivProtocol' is implied.
        authProtocol (tuple or ObjectIdentifier):
            An indication of whether messages sent on behalf of this USM user can be authenticated, and if so, the type of authentication protocol which is used.
            Supported authentication protocol identifiers are:
            * usmNoAuthProtocol         (default if *authKey* not given)
            * usmHMACMD5AuthProtocol    (default if *authKey* is given)
            * usmHMACSHAAuthProtocol
            * usmHMAC128SHA224AuthProtocol
            * usmHMAC192SHA256AuthProtocol
            * usmHMAC256SHA384AuthProtocol
            * usmHMAC384SHA512AuthProtocol
        authKeyType ():
            Type of `authKey` material. See RFC3414, section-2.6 for technical explanation.
            Supported key types are:
            * usmKeyTypePassphrase      (default)
            * usmKeyTypeMaster
            * usmKeyTypeLocalized
        privProtocol ():
            An indication of whether messages sent on behalf of this USM user be encrypted, and if so, the type of encryption protocol which is used.
            Supported encryption protocol identifiers are:
            * usmNoPrivProtocol         (default if *privhKey* not given)
            * usmDESPrivProtocol        (default if *privKey* is given)
            * usm3DESEDEPrivProtocol
            * usmAesCfb128Protocol
            * usmAesCfb192Protocol
            * usmAesCfb256Protocol
        privKeyType ():
            Type of `privKey` material. See RFC3414, section-2.6 for technical explanation.
            Supported key types are:
            * usmKeyTypePassphrase      (default)
            * usmKeyTypeMaster
            * usmKeyTypeLocalized
        securityEngineId (STR):
            The snmpEngineID of the authoritative SNMP engine to which a dateRequest message is to be sent
        securityName (STR):
            Together with the snmpEngineID it identifies a row in the 'usmUserTable' that is to be used for securing the message.

    Returns:
        Will return either a
        :py:class:`~pysnmp.hlapi.CommunityData` object instance for SNMP v1 or v2c, or a
        :py:class:`~pysnmp.hlapi.UsmUserData` object instance for SNMP v3
    """
    community_data_params = copy_keys(parameters,
        [
            'communityIndex', 'communityName', 'mpModel',
            'contextEngineId', 'contextName', 'tag'
        ]
    )
    usm_user_data_params = copy_keys(parameters,
        [
            'userName', 'securityEngineId', 'securityName',
            'authKey', 'authProtocol', 'authKeyType',
            'privKey', 'privProtocol', 'privKeyType'
        ]
    )

    snmp_protocol = parameters.get('snmp_protocol', '')

    if '3' in snmp_protocol:
        return UsmUserData(**usm_user_data_params)

    else:
        return CommunityData(
            **community_data_params,
            mpModel=0 if '1' in snmp_protocol else 1
        )


def transport_object(parameters) -> Union[UdpTransportTarget, Udp6TransportTarget, UnixTransportTarget]:
    """
    Return class instance representing Transport object instance.

    Parameters:
        transportAddr (tuple[FQDN: str, PORT: int]) :
            Remote (target) address, a tuple of (FQDN:str, PORT:int)
        localAddress (tuple[FQDN: str, PORT: int]) :
            Set local (source) address.
        timeout (int) :
            Response timeout in seconds.
        retries (int) :
            Maximum number of request retries, 0 retries means just a single request.
        tagList (str) :
            Arbitrary string that contains a list of space-separated tag strings used to select target addresses and/or SNMP configuration

    Options:
        use_ipv6 (bool) :
            Use IPv6, and return an Udp6TransportTarget object. If this flag is not set, an UdpTransportTarget (IPv4) will be returned.

    Returns:
        UdpTransportTarget instance
        or
        Udp6TransportTarget instance

    """
    transport_target_params = copy_keys(parameters,
        [
            'transportAddr', 'timeout', 'retries', 'tagList'
        ]
    )

    if parameters.get('use_ipv6'):
        transport = Udp6TransportTarget(**transport_target_params)

    else:
        transport = UdpTransportTarget(**transport_target_params)

    if localAddress := parameters.get('localAddress'):
        transport.setLocalAddress(localAddress)

    return transport


def context_object(parameters) -> ContextData:
    """
    Return a ContextData instance object with UDP/IPv6 configuration entry and initialize socket API if needed.
    See RFC3411 section-4.1 for SNMP Context details.

    Parameters:
        contextEngineId (str) :
            Uniquely identifies an SNMP entity that may realize an instance of a MIB with a particular contextName.
        contextName (str) :
            Used to name an instance of MIB. Default is empty string.

    Returns:
        ContextData: ContextData instance object
    """
    context_data_params = copy_keys(parameters,
        [
            'contextEngineId', 'contextName'
        ]
    )

    return ContextData(**context_data_params)

