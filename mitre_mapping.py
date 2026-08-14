def get_mitre_mapping(attack_type):

    mappings = {
        "SSH Brute Force": {
            "id": "T1110.001",
            "name": "Password Guessing",
            "tactic": "Credential Access"
        },

        "Username Enumeration": {
            "id": "T1110",
            "name": "Brute Force",
            "tactic": "Credential Access"
        },

        "Suspicious SSH Activity": {
            "id": "N/A",
            "name": "Unmapped",
            "tactic": "N/A"
        }
    }

    return mappings.get(
        attack_type,
        {
            "id": "N/A",
            "name": "Unmapped",
            "tactic": "N/A"
        }
    )
