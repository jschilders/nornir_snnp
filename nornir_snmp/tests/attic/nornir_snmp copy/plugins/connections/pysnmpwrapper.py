from pysnmp.hlapi import *

from .util import copy_keys, object_types, process_results


class pysnmpwrapper:
    def __init__(self, parameters):
        self.open(parameters)

    def open(self, parameters):
        self.parameters = parameters

        self.connection_params = [
            self.create_engine_object(),
            self.create_authentication_object(),
            self.create_transport_object(),
            self.create_context_object(),
        ]

    def close(self):
        self.parameters = {}
        self.connection_params = []

    def pysnmp_get(self, *args, **kwargs):
        yield from process_results(
            iterator=getCmd(
                *self.connection_params,
                *object_types(*args, **kwargs),
            )
        )

    def pysnmp_next(self, *args, lexicographicMode=False, **kwargs):
        yield from process_results(
            iterator=nextCmd(
                *self.connection_params,
                *object_types(*args, **kwargs),
                lexicographicMode=lexicographicMode,
            )
        )

    def pysnmp_bulk(
        self,
        *args,
        nonRepeaters=0,
        maxRepetitions=50,
        lexicographicMode=False,
        **kwargs,
    ):
        yield from process_results(
            iterator=bulkCmd(
                *self.connection_params,
                nonRepeaters,
                maxRepetitions,
                *object_types(*args, **kwargs),
                lexicographicMode=lexicographicMode,
            )
        )

    # 	def pysnmp_set(self, *args, **kwargs):
    # 		pass

    # 	def pysnmp_inform(self, *args, **kwargs):
    # 		pass

    # 	def pysnmp_trap(self, *args, **kwargs):
    # 		pass

    def create_engine_object(self):
        snmp_engine_params = copy_keys(self.parameters, ["snmpEngineID"])

        return SnmpEngine(**snmp_engine_params)

    def create_authentication_object(self):
        community_data_params = copy_keys(
            self.parameters,
            [
                "communityIndex",
                "communityName",
                "mpModel",
                "contextEngineId",
                "contextName",
                "tag",
            ],
        )

        usm_user_data_params = copy_keys(
            self.parameters,
            [
                "userName",
                "securityEngineId",
                "securityName",
                "authKey",
                "authProtocol",
                "authKeyType",
                "privKey",
                "privProtocol",
                "privKeyType",
            ],
        )

        snmp_protocol = self.parameters.get("snmp_protocol", "")

        if "3" in snmp_protocol:
            return UsmUserData(**usm_user_data_params)

        else:
            return CommunityData(
                **community_data_params, mpModel=0 if "1" in snmp_protocol else 1
            )

    def create_transport_object(self):
        transport_target_params = copy_keys(
            self.parameters, ["transportAddr", "timeout", "retries", "tagList"]
        )

        if self.parameters.get("use_ipv6", False):
            transport = Udp6TransportTarget(**transport_target_params)

        elif self.parameters.get("use_socket", False):
            transport = UnixTransportTarget(**transport_target_params)

        else:
            transport = UdpTransportTarget(**transport_target_params)

        if local_address := self.parameters.get("local_address", False):
            transport.setLocalAddress(local_address)

        return transport

    def create_context_object(self):
        context_data_params = copy_keys(
            self.parameters, ["contextEngineId", "contextName"]
        )

        return ContextData(**context_data_params)
