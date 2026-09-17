from datetime import datetime

class DriftDetector:
    def __init__(self, twin):
        self.twin = twin
        self.drifts = []
        print("[DRIFT DETECTOR] Initialized successfully")

    def detect_drift(self):
        self.drifts = []
        resources = self.twin.get_all_resources()
        baselines = self.twin.get_baselines()

        for resource_id, resource_data in resources.items():
            resource_type = resource_data["resource_type"]
            current_config = resource_data["config"]

            if resource_type in baselines:
                baseline = baselines[resource_type]
                for parameter, expected_value in baseline.items():
                    current_value = current_config.get(parameter)
                    if current_value != expected_value:
                        drift = {
                            "resource_id": resource_id,
                            "resource_type": resource_type,
                            "parameter": parameter,
                            "expected": expected_value,
                            "found": current_value,
                            "severity": self.calculate_severity(parameter),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "remediation": self.get_remediation(parameter, expected_value)
                        }
                        self.drifts.append(drift)
                        print(f"[DRIFT DETECTED] {resource_id} -> {parameter} (Severity: {drift['severity']})")

        return self.drifts

    def calculate_severity(self, parameter):
        critical = ["public_access", "admin_access", "encryption",
                   "ssh_open_to_all", "rdp_open_to_all", "public_ip_exposed",
                   "all_traffic_allowed", "ssl_enforced"]
        high = ["mfa_enabled", "least_privilege", "outbound_restricted",
               "encryption_at_rest", "access_key_age_days"]
        medium = ["logging", "versioning", "monitoring_enabled",
                 "backup_enabled", "unused_credentials_removed", "os_patched"]

        if parameter in critical:
            return "CRITICAL"
        elif parameter in high:
            return "HIGH"
        elif parameter in medium:
            return "MEDIUM"
        else:
            return "LOW"

    def get_remediation(self, parameter, expected_value):
        remediations = {
            "public_access": "Disable public access immediately on this resource",
            "admin_access": "Remove admin permissions and apply least privilege",
            "encryption": "Enable encryption on this resource immediately",
            "ssh_open_to_all": "Restrict SSH access to specific IP ranges only",
            "rdp_open_to_all": "Restrict RDP access to specific IP ranges only",
            "mfa_enabled": "Enable Multi-Factor Authentication for this account",
            "logging": "Enable logging and monitoring on this resource",
            "versioning": "Enable versioning to protect against accidental deletion",
            "monitoring_enabled": "Enable monitoring and alerting on this resource",
            "public_ip_exposed": "Remove public IP or place behind load balancer",
            "backup_enabled": "Enable automated backups for disaster recovery",
            "os_patched": "Apply latest security patches immediately"
        }
        return remediations.get(parameter, f"Set {parameter} to {expected_value}")

    def get_drifts(self):
        return self.drifts
