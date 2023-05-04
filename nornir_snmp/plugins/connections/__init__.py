from nornir.core.configuration import Config
from typing import Any, Optional

from nornir_snmp.plugins.connections.pysnmpwrapper import pysnmpwrapper

CONNECTION_NAME = "SNMP"


class SNMP:
    def open(
        self,   
        hostname:       Optional[str],
        username:       Optional[str],
        password:       Optional[str],
        port:           Optional[int],
        platform:       Optional[str],
        extras:         Optional[dict[str, Any]],
        configuration:  Optional[Config],
    ) -> None:
        """
        Initialize SNMP class instance

        Args:

        Args come from the standard options of the Nornir inventory. Not all are applicable 
        for SNMP, but all are listed here to present a uniform interface to Nornir
        
        hostname (Optional[str]):           Hostname to connect to
        username (Optional[str]):           Username
        password (Optional[str]):           Password for user. Used as communitystring for SNMP v1/v2c if not overridden
        port (Optional[int]):               UDP Port to use for SNMP connection. Defaults to 161
        platform (Optional[str]):           Platform of target machine, i.e. IOS or Junos. Not used.
        extras (Optional[dict]):            'connection_options.SNMP' key in Nornir inventory with (extra) parameters to initialize
                                            the pysnmpwrapper class instance. Below are some of the more common parameters. 
                                            For more information, see the pysnmpwrapper class documentation.

                                            Authentication parameters::
                                                snmp_protocol (str):        SNMP Protocol to use. 'V1', 'V2c' or 'V3' suggested, 
                                                                            but any string containing a 1, 2 or 3 will do.

                                                Parameters for SNMP V1/V2c:
                                                    communityName (str):    SNMP v1/v2c community string

                                                Parameters for SNMP V3:
                                                    userName (str):         The name of the SNMP USM user
                                                    authKey (str):          The secret authentication key.
                                                    privKey (str):          The secret encryption key.
                                                    authProtocol (tuple):   The type of authentication protocol which is used.
                                                    privProtocol (tuple):   The type of encryption protocol which is used.


                                            Transport Parameters:
                                                transportAddr (tuple):      Remote (target) address, a tuple of (FQDN:str, PORT:int)
                                                localAddress (tuple):       Set local (source) address, a tuple of (FQDN:str, PORT:int)
                                                timeout (int) :             Response timeout in seconds.
                                                retries (int) :             Maximum number of request retries, 0 retries means just a single request.
                                                use_ipv6 (bool) :           Use IPv6, and return an Udp6TransportTarget object. If this flag
                                                                            is not set, an UdpTransportTarget (IPv4) will be returned.


        configuration (Optional[Config]):   Nornir configuration object. Not used.

        Example inventory item:

        some_host_name:
            hostname: some_host_name
            port:     161
            username: some_random_user
            password: secret_password
            platform: junos
            groups:   [...]
            data:     [...]
            connection_options:
                SNMP:
                    extras:
                        snmp_protocol:  v2c
                        communityName:  '@c1sc0atl45t'
                        transportAddr:  [some.host.name, 161]

            parameters listed under connection_options.SNMP.extras will override host parameters.
            connection_options can also come from group or default entries (see Nornir inventory documentation)
        """

        #
        # Try to get some sensible values out of the standard connection parrameters, in case there are no 'connection_parameters' options. 
        # Use hostname and port for transportaddr, and the password as the community string. This is enough for SNMP v1/v2c.
        # These will be overridden by parameters specified in the 'extras' dict
        #
        parameters = {
            'communityIndex':   None,
            'communityName':    password,
            'transportAddr':    (hostname, port or 161),
        }
        #
        # Override with parameters from 'connection_parameters'
        #
        parameters.update(extras or {})
        
        connection = pysnmpwrapper(parameters)

        self.connection = connection


    def close(self) -> None:
        pass