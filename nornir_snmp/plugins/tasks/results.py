from typing import Iterator
from pysnmp.smi.rfc1902 import ObjectType
from pysnmp.error import PySnmpError
from pysnmp.smi.exval import endOfMibView


def endOfMib(varBind):
    return endOfMibView.isSameTypeWith(varBind[1])
    # return endOfMib == varBind[1]


def get_results(iterator: Iterator) -> ObjectType:

    results = []
    count = 0
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            raise PySnmpError(errorIndication)
        elif errorStatus:
            errorMessage = errorStatus.prettyPrint()
            errorLocation = varBinds[int(errorIndex) - 1][0] if errorIndex else "?"
            raise PySnmpError(f"{errorMessage} at {errorLocation}")

        for varBind in varBinds:
            if not endOfMib(varBind):
                results.append(varBind.prettyPrint())

    return results