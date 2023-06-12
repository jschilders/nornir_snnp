from typing import Union
from pysnmp.hlapi.asyncore.sync import getCmd, nextCmd, bulkCmd, setCmd, sendNotification
from pysnmp.smi.rfc1902 import ObjectIdentity, ObjectType
from pysnmp.entity.engine import SnmpEngine
from pysnmp.hlapi.auth import CommunityData, UsmUserData
from pysnmp.hlapi.asyncore.transport import UnixTransportTarget, Udp6TransportTarget, UdpTransportTarget
from pysnmp.hlapi.context import ContextData
from pysnmp.hlapi.varbinds import AbstractVarBinds

copy_keys = lambda s, l: {k: v for k, v in s.items() if k in l}

class pysnmpwrapper:

    def __init__(self, parameters: dict) -> None:
        """Initializes self.connection_params instance variable.

        Initializes:
            self.connection_params[
                snmpEngine (SnmpEngine) :
                    Class instance representing SNMP engine.
                authData (CommunityData or UsmUserData) :
                    Class instance representing SNMP credentials.
                transportTarget (UdpTransportTarget or Udp6TransportTarget) :
                    Class instance representing transport type along with SNMP peer address.
                contextData (ContextData) :
                    Class instance representing SNMP ContextEngineId and ContextName values.
            ]

        Args:
            parameters (dict): Dictionairy containing parameters for initialisation.

            SnmpEngine parameters:
                snmpEngineID (str) :
                    Optional engine ID

            Authentication parameters::
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
                        * usmNoAuthProtocol         (default is *authKey* not given)
                        * usmHMACMD5AuthProtocol    (default if *authKey* is given)
                        * usmHMACSHAAuthProtocol
                        * usmHMAC128SHA224AuthProtocol
                        * usmHMAC192SHA256AuthProtocol
                        * usmHMAC256SHA384AuthProtocol
                        * usmHMAC384SHA512AuthProtocol
                    authKeyType (tuple or ObjectIdentifier):
                        Type of `authKey` material. See RFC3414, section-2.6 for technical explanation.
                        Supported key types are:
                        * usmKeyTypePassphrase      (default)
                        * usmKeyTypeMaster
                        * usmKeyTypeLocalized
                    privProtocol (tuple or ObjectIdentifier):
                        An indication of whether messages sent on behalf of this USM user be encrypted, and if so, the type of encryption protocol which is used.
                        Supported encryption protocol identifiers are:
                        * usmNoPrivProtocol         (default is *privhKey* not given)
                        * usmDESPrivProtocol        (default if *privKey* is given)
                        * usm3DESEDEPrivProtocol
                        * usmAesCfb128Protocol
                        * usmAesCfb192Protocol
                        * usmAesCfb256Protocol
                    privKeyType (tuple or ObjectIdentifier):
                        Type of `privKey` material. See RFC3414, section-2.6 for technical explanation.
                        Supported key types are:
                        * usmKeyTypePassphrase      (default)
                        * usmKeyTypeMaster
                        * usmKeyTypeLocalized
                    securityEngineId (STR):
                        The snmpEngineID of the authoritative SNMP engine to which a dateRequest message is to be sent
                    securityName (STR):
                        Together with the snmpEngineID it identifies a row in the 'usmUserTable' that is to be used for securing the message.

            Transport Parameters:
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
                use_ipv6 (bool) :
                    Use IPv6, and return an Udp6TransportTarget object. If this flag is not set, an UdpTransportTarget (IPv4) will be returned.

            Context Parameters:
                contextEngineId (str) :
                    Uniquely identifies an SNMP entity that may realize an instance of a MIB with a particular contextName.
                contextName (str) :
                    Used to name an instance of MIB. Default is empty string.
        """

        self.parameters = parameters

        self.connection_params = [
            self.engine_object(),
            self.authentication_object(),
            self.transport_object(),
            self.context_object()
        ]


    def engine_object(self) -> SnmpEngine:
        """Return class instance representing SNMP engine

        Parameters:
            snmpEngineID (str) :
                Optional engine ID

        Returns:
            SnmpEngine: Class instance representing SNMP engine
        """
        snmp_engine_params = copy_keys(self.parameters,
            [
                'snmpEngineID'
            ]
        )

        return SnmpEngine(**snmp_engine_params)


    def authentication_object(self) -> Union[CommunityData, UsmUserData]:
        """Return class instance representing SNMP credentials.

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
            Will return either a CommunityData object instance for SNMP v1 or v2c, or a UsmUserData` object instance for SNMP v3
        """
        community_data_params = copy_keys(self.parameters,
            [
                'communityIndex', 'communityName', 'mpModel',
                'contextEngineId', 'contextName', 'tag'
            ]
        )
        usm_user_data_params = copy_keys(self.parameters,
            [
                'userName', 'securityEngineId', 'securityName',
                'authKey', 'authProtocol', 'authKeyType',
                'privKey', 'privProtocol', 'privKeyType'
            ]
        )

        snmp_protocol = self.parameters.get('snmp_protocol', '')

        if '3' in snmp_protocol:
            return UsmUserData(**usm_user_data_params)
        else:
            return CommunityData(
                **community_data_params,
                mpModel=0 if '1' in snmp_protocol else 1
            )


    def transport_object(self) -> Union[UdpTransportTarget, Udp6TransportTarget, UnixTransportTarget]:
        """Return class instance representing Transport object instance.

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
                Use IPv6, and return an Udp6TransportTarget object.
            use_socket (bool) :
                Use unix socket, and return an UnixTransportTarget object. 
            If neither flag is set, an UdpTransportTarget (IPv4) will be returned.

        Returns:
            Instance object of type {Udp,Udp6,Unix}TransportTarget

        """
        transport_target_params = copy_keys(self.parameters,
            [
                'transportAddr', 'timeout', 'retries', 'tagList'
            ]
        )

        if self.parameters.get('use_socket'):
            transport = UnixTransportTarget(**transport_target_params)
        elif self.parameters.get('use_ipv6'):
            transport = Udp6TransportTarget(**transport_target_params)
        else:
            transport = UdpTransportTarget(**transport_target_params)

        if localAddress := self.parameters.get('localAddress'):
            transport.setLocalAddress(localAddress)

        return transport


    def context_object(self) -> ContextData:
        """Return class instance representing ContextData object instance.

        Parameters:
            contextEngineId (str) :
                Uniquely identifies an SNMP entity that may realize an instance of a MIB with a particular contextName.
            contextName (str) :
                Used to name an instance of MIB. Default is empty string.

        Returns:
            ContextData: ContextData instance object
        """
        context_data_params = copy_keys(self.parameters,
            [
                'contextEngineId', 'contextName'
            ]
        )

        return ContextData(**context_data_params)


    def mibviewcontroller(self):
        """Return class instance representing MibViewController object instance

        Returns:
            MibViewControler: MibViewController instance object
        """
        try:
            snmp_engine = self.connection_params[0]
            return AbstractVarBinds.getMibViewController(snmp_engine)
        except (NameError, IndexError):
            raise LookupError("pysnmpwrapper object instance is not initialized")
  

    def pysnmp_get(self, *varbinds, **options) -> list[ObjectType]:
        """Wrapper for the pysnmp.hlapi.getCmd method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.

            See 'resolveMibs' documentation for recognized OID formats and extra options.
            
        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.
        """
        return getCmd(*self.connection_params, *varbinds, **options)


    def pysnmp_set(self, *varbinds, **options) -> list[ObjectType]:
        """Wrapper for the pysnmp.hlapi.setCmd method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.
            payload ()
                ...
                
            See 'resolveMibs' documentation for recognized OID formats and extra options.
            
        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.
        """
        return setCmd(*self.connection_params, *varbinds, **options)


    def pysnmp_next(self, *varbinds, lexicographicMode: bool=False, **options) -> list[ObjectType]:
        """Wrapper for the pysnmp.hlapi.nextCmd method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.

            See 'resolveMibs' documentation for recognized OID formats and extra options.

        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.
            lexicographicMode : bool
                walk SNMP agent's MIB till the end (if `True`), otherwise (if `False`) stop iteration when all response MIB variables leave the scope of initial MIB variables in `varBinds`. Default is `False`.
            ignoreNonIncreasingOid : bool
                continue iteration even if response MIB variables (OIDs) are not greater then request MIB variables. Be aware that setting it to `True` may cause infinite loop between SNMP management and agent applications. Default is `False`.
            maxRows : int
                stop iteration once this generator instance processed `maxRows` of SNMP conceptual table. Default is `0` (no limit).
            maxCalls : int
                stop iteration once this generator instance processed `maxCalls` responses. Default is 0 (no limit).

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.

        """
        return nextCmd(*self.connection_params, *varbinds, lexicographicMode=lexicographicMode, **options)


    def pysnmp_bulk(self, *varbinds, nonRepeaters: int=0, maxRepetitions: int=50, lexicographicMode: bool=False,  **options) -> list[ObjectType]:
        """Wrapper for the pysnmp.hlapi.bulkCmd method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.

            See 'resolveMibs' documentation for recognized OID formats and extra options.

            nonRepeaters : int
                One MIB variable is requested in response for the first `nonRepeaters` MIB variables in request. Defaults to 0.
            maxRepetitions : int
                `maxRepetitions` MIB variables are requested in response for each of the remaining MIB variables in the request. Defaults to 50.

            if you provide a list of OID's to get, then the first <nonRepeaters> number of OID's in that list will be retrieved with a simple getCmd, 
            while for the rest of the OID's in that list, variables will be retrieved in chunks of <maxRepetitions> items, until all the OID's are exhausted.
            
        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.
            lexicographicMode : bool
                walk SNMP agent's MIB till the end (if `True`), otherwise (if `False`) stop iteration when all response MIB variables leave the scope of initial MIB variables in `varBinds`. Default is `False`.
            ignoreNonIncreasingOid : bool
                continue iteration even if response MIB variables (OIDs) are not greater then request MIB variables. Default is `False`.
            maxRows : int
                stop iteration once this generator instance processed `maxRows` of SNMP conceptual table. Default is `0` (no limit).
            maxCalls : int
                stop iteration once this generator instance processed `maxCalls` responses. Default is 0 (no limit).

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.
        """
        return bulkCmd(*self.connection_params, nonRepeaters, maxRepetitions, *varbinds, lexicographicMode=lexicographicMode, **options)


    def pysnmp_inform(self, *varbinds, **options):
        """Wrapper for the pysnmp.hlapi.sendNotification method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.

            See 'resolveMibs' documentation for recognized OID formats and extra options.
            
        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.
        """
        return sendNotification(*self.connection_params, 'inform', *varbinds, **options)


    def pysnmp_trap(self, *varbinds, **options):
        """Wrapper for the pysnmp.hlapi.sendNotification method.

        Args:
            oid (tuple or str):
                single MIB variable identity.
            oids (list[oid]):
                list of MIB variable identities.

            See 'resolveMibs' documentation for recognized OID formats and extra options.
            
        Gnerator Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.

        Yields:
            Iterator[ObjectType]:
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.
        """
        return sendNotification(*self.connection_params, 'trap', *varbinds, **options)

