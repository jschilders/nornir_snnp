from pysnmp.hlapi import *
from nornir_snmp.plugins.connections.util import copy_keys, generator_options, varbinds_options, ResolveMibs, process_results
from typing import Any, Optional, Union


class pysnmpwrapper:

    # --------------------------------------
    # nornir_snmp -> pysnmpwrapper interface
    # --------------------------------------

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
            self.create_engine_object(),
            self.create_authentication_object(),
            self.create_transport_object(),
            self.create_context_object(),
        ]


    def pysnmp_get(self, **kwargs: dict) -> list[ObjectType]:
        """
        Wrapper for the pysnmp.hlapi.getCmd method.

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
                
            Recognized variants for MIB variable identity:
                - a tuple of integers representing OID.
                - a str representing OID in dot-separated integers form.
                - a str representing MIB variable in dot-separated labels form.
                - a str representing MIB name. First variable defined in MIB is assumed.
                - a tuple of str representing MIB name and variable name.
                - a tuple of str representing MIB name and variable name, followed by any number of indexes.
                - a predefined or configured ObjectType instance object.

        Options:
            lookupMib : bool
                load MIB and resolve response MIB variables at the cost of slightly reduced performance. Default is `True`.
            resolveWithMib (bool, default=True):
                Perform MIB variable ID conversion.
                Options: ignoreErrors (bool, default=True)

        Yields:
            Iterator[ObjectType]: 
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.

        """
        yield from process_results(
            getCmd(
                *self.connection_params,
                *ResolveMibs(**kwargs),
                **generator_options(kwargs)
            )
        )


    def pysnmp_next(self, **kwargs: dict) -> list[ObjectType]:
        """
        Wrapper for the pysnmp.hlapi.nextCmd method.

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
                
            Recognized variants for MIB variable identity:
                - a tuple of integers representing OID.
                - a str representing OID in dot-separated integers form.
                - a str representing MIB variable in dot-separated labels form.
                - a str representing MIB name. First variable defined in MIB is assumed.
                - a tuple of str representing MIB name and variable name.
                - a tuple of str representing MIB name and variable name, followed by any number of indexes.
                - a predefined or configured ObjectType instance object.

        Options:
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
            resolveWithMib (bool, default=True):
                Perform MIB variable ID conversion.
                Options: ignoreErrors (bool, default=True)

        Yields:
            Iterator[ObjectType]: 
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.

        """
        yield from process_results(
            nextCmd(
                *self.connection_params,
                *ResolveMibs(**kwargs),
                **generator_options(kwargs)
            )
        )


    def pysnmp_bulk(self, nonRepeaters: int=0, maxRepetitions: int=50, **kwargs) -> list[ObjectType]:
        """
        Wrapper for the pysnmp.hlapi.bulkCmd method.

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
                
            Recognized variants for MIB variable identity:
                - a tuple of integers representing OID.
                - a str representing OID in dot-separated integers form.
                - a str representing MIB variable in dot-separated labels form.
                - a str representing MIB name. First variable defined in MIB is assumed.
                - a tuple of str representing MIB name and variable name.
                - a tuple of str representing MIB name and variable name, followed by any number of indexes.
                - a predefined or configured ObjectType instance object.

        Options:
            nonRepeaters : int
                One MIB variable is requested in response for the first `nonRepeaters` MIB variables in request. Defaults to 0.
            maxRepetitions : int
                `maxRepetitions` MIB variables are requested in response for each of the remaining MIB variables in the request. Defaults to 50.
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
            resolveWithMib (bool, default=True):
                Perform MIB variable ID conversion.
                Options: ignoreErrors (bool, default=True)

        Yields:
            Iterator[ObjectType]: 
                Sequence of ObjectType class instances representing MIB variables returned in SNMP response.

        """
        yield from process_results(
            bulkCmd(
                *self.connection_params,
                nonRepeaters,
                maxRepetitions,
                *ResolveMibs(**kwargs),
                **generator_options(kwargs)

            )
        )


    # 	def pysnmp_set(self, **kwargs) -> list[ObjectType]:
    # 		pass


    # 	def pysnmp_inform(self, **kwargs) -> list[ObjectType]:
    # 		pass


    # 	def pysnmp_trap(self, **kwargs) -> list[ObjectType]:
    # 		pass


    def create_engine_object(self) -> SnmpEngine:
        """
        Return class instance representing SNMP engine

        Parameters:
            snmpEngineID (str) :
                Optional engine ID
                
        Returns:
            SnmpEngine (:py:class:`~pysnmp.hlapi.SnmpEngine`): Class instance representing SNMP engine
        """
        snmp_engine_params = copy_keys(self.parameters,
            [
                'snmpEngineID'
            ]
        )

        return SnmpEngine(**snmp_engine_params)


    def create_authentication_object(self) -> Union[CommunityData, UsmUserData]:
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


    def create_transport_object(self) -> Union[UdpTransportTarget, Udp6TransportTarget, UnixTransportTarget]:
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
        transport_target_params = copy_keys(
            self.parameters,
            [
                'transportAddr', 'timeout', 'retries', 'tagList'
            ]
        )

        if self.parameters.get('use_ipv6'):
            transport = Udp6TransportTarget(**transport_target_params)

        else:
            transport = UdpTransportTarget(**transport_target_params)

        if localAddress := self.parameters.get('localAddress'):
            transport.setLocalAddress(localAddress)

        return transport


    def create_context_object(self) -> ContextData:
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
        context_data_params = copy_keys(
            self.parameters,
            [
                'contextEngineId', 'contextName'
            ]
        )

        return ContextData(**context_data_params)
