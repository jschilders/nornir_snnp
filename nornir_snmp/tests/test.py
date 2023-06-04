from pysnmp.hlapi import *

g = nextCmd(SnmpEngine(),
    CommunityData('@c1sc0atl45t'),
    UdpTransportTarget(('cr1.eqam8', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('IF-MIB', 'ifDescr')))