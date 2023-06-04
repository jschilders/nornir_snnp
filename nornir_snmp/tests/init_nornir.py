from nornir import InitNornir

def nornir_inventory():
    return InitNornir(
        runner={
            "plugin": "threaded",
            "options": {
                "num_workers": 20,
            },
        },
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file":        "/opt/nornir/nornir_snmp/nornir_snmp/tests/inventory/hosts.yaml",
                "group_file":       "/opt/nornir/nornir_snmp/nornir_snmp/tests/inventory/groups.yaml",
                "defaults_file":    "/opt/nornir/nornir_snmp/nornir_snmp/tests/inventory/defaults.yaml",
            },
        },
    )
