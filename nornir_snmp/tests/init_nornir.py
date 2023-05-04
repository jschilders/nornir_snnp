from nornir import InitNornir

def nornir_inventory():
    return InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 100,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file":        "/opt/nornir/nornir_snmp/nornir_snmp/tests/inventory/hosts.yaml",
                "defaults_file":    "/opt/nornir/nornir_snmp/nornir_snmp/tests/inventory/defaults.yaml",
            },
        },
    )
