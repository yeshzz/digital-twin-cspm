def scenario_1_public_s3(twin):
    print("\n[SCENARIO 1] S3 Bucket made PUBLIC - Critical Attack")

    twin.update_resource("s3-prod-data", {
        "public_access": True
    })

def scenario_2_admin_iam(twin):
    print("\n[SCENARIO 2] IAM Role given ADMIN ACCESS - Critical Attack")
    twin.update_resource("iam-developer-role", {
        "admin_access": True,
        "mfa_enabled": True,
        "access_key_age_days": 90,
        "unused_credentials_removed": True,
        "least_privilege": False
    })

def scenario_3_ssh_open(twin):
    print("\n[SCENARIO 3] SSH Port opened to ALL IPs - High Attack")
    twin.update_resource("sg-web-server", {
        "ssh_open_to_all": True,
        "rdp_open_to_all": False,
        "all_traffic_allowed": False,
        "unused_ports_open": False,
        "outbound_restricted": True
    })

def scenario_4_encryption_disabled(twin):
    print("\n[SCENARIO 4] Encryption DISABLED on S3 - Critical Attack")
    twin.update_resource("s3-prod-data", {
        "public_access": False,
        "encryption": False,
        "versioning": True,
        "logging": True,
        "ssl_enforced": True
    })

def scenario_5_monitoring_off(twin):
    print("\n[SCENARIO 5] Monitoring DISABLED on VM - Medium Attack")

    twin.update_resource("vm-app-server", {
        "monitoring_enabled": False
    })

def reset_all(twin):
    print("\n[RESET] Restoring all resources to secure baseline")
    twin.update_resource("s3-prod-data", {
        "public_access": False,
        "encryption": True,
        "versioning": True,
        "logging": True,
        "ssl_enforced": True
    })
    twin.update_resource("iam-developer-role", {
        "admin_access": False,
        "mfa_enabled": True,
        "access_key_age_days": 90,
        "unused_credentials_removed": True,
        "least_privilege": True
    })
    twin.update_resource("sg-web-server", {
        "ssh_open_to_all": False,
        "rdp_open_to_all": False,
        "all_traffic_allowed": False,
        "unused_ports_open": False,
        "outbound_restricted": True
    })
    twin.update_resource("vm-app-server", {
        "public_ip_exposed": False,
        "os_patched": True,
        "monitoring_enabled": True,
        "encryption_at_rest": True,
        "backup_enabled": True
    })
