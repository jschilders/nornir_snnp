from pysnmp.hlapi import *
from pysnmp.smi.view import MibViewController
from pysnmp.smi.builder import MibBuilder


from .util import functionwrapper, copy_keys, make_varBinds, process_results

class pysnmpwrapper:

	def __init__(self, parameters):

		self.parameters = parameters
  
		self.engine_object =         self.create_engine_object(),
		self.authentication_object = self.create_authentication_object(),
		self.transport_object =      self.create_transport_object(),
		self.context_object =        self.create_context_object()
		self.mibview_object =        self.create_mibview_object()

		self.connection_params = [
			self.engine_object,
			self.authentication_object,
			self.transport_object,
			self.context_object
		]


	def snmp_get(self, *args, **kwargs):
		iterator = getCmd(
      		*self.connection_params, 
        	*make_varBinds(*args[1:], **kwargs)
         )
		yield from process_results(iterator)


	def snmp_get(self, *args, **kwargs):
		yield from process_results(		
            iterator = getCmd(
      			*self.connection_params, 
        		*make_varBinds(*args[1:], **kwargs)
         	)
		)


	@functionwrapper
	def snmp_get(self, *args, varBind=None, **kwargs):
		return getCmd(*self.connection_params, *varBind)


	@functionwrapper
	def snmp_next(self, *args, varBind=None, **kwargs):
		return nextCmd(*self.connection_params, *varBind)


	def snmp_bulk(self, *args, **kwargs):
		pass


	def snmp_set(self, *args, **kwargs):
		pass


	def snmp_inform(self, *args, **kwargs):
		pass


	def snmp_trap(self, *args, **kwargs):
		pass


	def test():
		pass


	def create_engine_object(self):

		snmp_engine_params = copy_keys(self.parameters, [
	  		'snmpEngineID'
		])

		return SnmpEngine(**snmp_engine_params)


	def create_authentication_object(self):

		community_data_params = copy_keys(self.parameters, [
			'communityIndex', 'communityName', 'mpModel', 'contextEngineId', 'contextName', 'tag'
		])

		usm_user_data_params = copy_keys(self.parameters,  [
			'userName', 'securityEngineId', 'securityName', 'authKey', 'authProtocol', 'authKeyType', 'privKey', 'privProtocol', 'privKeyType',
		])

		snmp_protocol = self.parameters.get('snmp_protocol', '')

		if '3' in snmp_protocol:
			return UsmUserData(**usm_user_data_params)

		else:
			return CommunityData(**community_data_params, mpModel = 0 if '1' in snmp_protocol else 1)


	def create_transport_object(self):

		transport_target_params = copy_keys(self.parameters, [
	  		'transportAddr', 'timeout', 'retries', 'tagList'
		])

		if self.parameters.get('use_ipv6', False):
			transport = Udp6TransportTarget(**transport_target_params)

		elif self.parameters.get('use_socket', False):
			transport = UnixTransportTarget(**transport_target_params)

		else:
			transport = UdpTransportTarget(**transport_target_params)

		if local_address :=self.parameters.get('local_address', False):
			transport.setLocalAddress(local_address)

		return transport


	def create_context_object(self):

		context_data_params = copy_keys(self.parameters, [
	  		'contextEngineId', 'contextName'
		])

		return ContextData(**context_data_params)


	def create_mibview_object(self):

		#context_data_params = copy_keys(self.parameters, ['contextEngineId', 'contextName'])

		return MibViewController(MibBuilder)


		#mibViewController = varbinds.AbstractVarBinds.getMibViewController( engine )
