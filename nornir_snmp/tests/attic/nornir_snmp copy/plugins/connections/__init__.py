from nornir.core.configuration import Config
from typing import Any, Dict, Optional

from .pysnmpwrapper import pysnmpwrapper

CONNECTION_NAME = "SNMP"


class SNMP:
    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]],
        configuration: Optional[Config],
    ) -> None:
        parameters = {
            "communityIndex": None,
            "communityName": password,
            "transportAddr": (hostname, port or 161),
        }

        extras = extras or {}
        parameters.update(extras)

        connection = pysnmpwrapper(parameters)

        self.connection = connection

    def close(self) -> None:
        self.connection.close()
