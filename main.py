import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from digital_twin.twin_core import DigitalTwin
from digital_twin.drift_detector import DriftDetector
from digital_twin.risk_scorer import RiskScorer
from digital_twin.alert_system import AlertSystem
from simulations.attack_scenarios import *

def initialize_resources(twin):
    print("\n[SETUP] Loading cloud resources into Digital Twin...")

    twin.add_resource("s3-prod-data", "S3_Bucket", {
        "public_access": False,
        "encryption": True,
        "versioning": True,
        "logging": True,
        "ssl_enforced": True
    })

    twin.add_resource("iam-developer-role", "IAM_Role", {
        "admin_access": False,
        "mfa_enabled": True,
        "access_key_age_days": 90,
        "unused_credentials_removed": True,
        "least_privilege": True
    })

    twin.add_resource("sg-web-server", "Security_Group", {
        "ssh_open_to_all": False,
        "rdp_open_to_all": False,
        "all_traffic_allowed": False,
        "unused_ports_open": False,
        "outbound_restricted": True
    })

    twin.add_resource("vm-app-server", "VM_Instance", {
        "public_ip_exposed": False,
        "os_patched": True,
        "monitoring_enabled": True,
        "encryption_at_rest": True,
        "backup_enabled": True
    })

    print(f"[SETUP] {len(twin.get_all_resources())} resources loaded successfully")

def run_scan(twin, detector, scorer, alert_system, scenario_name="Manual Scan"):
    print(f"\n{'='*60}")
    print(f"SCANNING: {scenario_name}")
    print(f"{'='*60}")

    drifts = detector.detect_drift()
    score = scorer.calculate_posture_score(drifts)
    risk_level = scorer.get_risk_level(score)
    severity_summary = scorer.get_severity_summary(drifts)
    alerts = alert_system.generate_alerts(drifts)

    print(f"\n POSTURE SCORE: {score}/100 — {risk_level}")
    print(f" Drifts Found: {len(drifts)}")
    print(f" Critical: {severity_summary['CRITICAL']} | High: {severity_summary['HIGH']} | Medium: {severity_summary['MEDIUM']} | Low: {severity_summary['LOW']}")
    print(f" Alerts Fired: {len(alerts)}")

    if drifts:
        print(f"\n DRIFT DETAILS:")
        for drift in drifts:
            print(f"  [{drift['severity']}] {drift['resource_id']} -> {drift['parameter']}")
            print(f"    Expected: {drift['expected']} | Found: {drift['found']}")
            print(f"    Fix: {drift['remediation']}")

    return score, drifts

def main():
    print("\n" + "="*60)
    print("  DIGITAL TWIN — CLOUD SECURITY POSTURE & DRIFT DETECTION")
    print("  IIIT Trichy Funded Research Project")
    print("  Researcher: Yashaswini C")
    print("="*60)

    twin = DigitalTwin()
    detector = DriftDetector(twin)
    scorer = RiskScorer()
    alert_system = AlertSystem()

    initialize_resources(twin)

    print("\n" + "="*60)
    print("SELECT MODE:")
    print("1. Run All 5 Attack Scenarios Automatically")
    print("2. Run Individual Scenario")
    print("3. Launch Web Dashboard")
    print("4. Run Chained Attack Sequence")
    print("5. Run Frequency Probe Demo")
    print("="*60)
    choice = input("Enter choice (1/2/3/4/5): ").strip()

    if choice == "1":
        run_scan(twin, detector, scorer, alert_system, "Baseline Scan - All Secure")

        scenario_1_public_s3(twin)
        run_scan(twin, detector, scorer, alert_system, "Scenario 1 - S3 Public Exposure")

        reset_all(twin)
        scenario_2_admin_iam(twin)
        run_scan(twin, detector, scorer, alert_system, "Scenario 2 - IAM Admin Access")

        reset_all(twin)
        scenario_3_ssh_open(twin)
        run_scan(twin, detector, scorer, alert_system, "Scenario 3 - SSH Open to All")

        reset_all(twin)
        scenario_4_encryption_disabled(twin)
        run_scan(twin, detector, scorer, alert_system, "Scenario 4 - Encryption Disabled")

        reset_all(twin)
        scenario_5_monitoring_off(twin)
        run_scan(twin, detector, scorer, alert_system, "Scenario 5 - Monitoring Disabled")

        reset_all(twin)
        run_scan(twin, detector, scorer, alert_system, "Final Scan - All Restored")

    elif choice == "2":
        print("\nScenarios:")
        print("1. S3 Bucket Public Exposure")
        print("2. IAM Admin Access")
        print("3. SSH Open to All IPs")
        print("4. Encryption Disabled")
        print("5. Monitoring Disabled")
        s = input("Choose scenario (1-5): ").strip()
        scenarios = {
            "1": scenario_1_public_s3,
            "2": scenario_2_admin_iam,
            "3": scenario_3_ssh_open,
            "4": scenario_4_encryption_disabled,
            "5": scenario_5_monitoring_off
        }
        if s in scenarios:
            scenarios[s](twin)
            run_scan(twin, detector, scorer, alert_system, f"Scenario {s}")

    elif choice == "3":
        print("\n[DASHBOARD] Launching web dashboard...")
        print("[DASHBOARD] Open browser and go to: http://127.0.0.1:5000")
        print("[DASHBOARD] Press CTRL+C in terminal to stop")
        from dashboard.app import create_app
        app = create_app(twin, detector, scorer, alert_system)
        app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5000)


    
    elif choice == "4":
        print("\n[CHAINED ATTACK] Running full attack sequence")
        print("[CHAINED ATTACK] Score will be recorded after each step")

        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Baseline - All Secure"
        )

        print("\n[CHAIN Step 1] Attacker opens SSH port - initial foothold")
        scenario_3_ssh_open(twin)
        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Step 1 - SSH Open"
        )

        print("\n[CHAIN Step 2] Attacker escalates IAM privileges - privilege escalation")
        scenario_2_admin_iam(twin)
        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Step 2 - IAM Admin Access"
        )

        print("\n[CHAIN Step 3] Attacker disables encryption - data protection weakened")
        scenario_4_encryption_disabled(twin)
        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Step 3 - Encryption Disabled"
        )

        print("\n[CHAIN Step 4] Attacker exposes S3 - data exposure")
        scenario_1_public_s3(twin)
        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Step 4 - S3 Public Exposure"
        )

        print("\n[CHAIN Step 5] Attacker disables monitoring - covering tracks")
        scenario_5_monitoring_off(twin)
        run_scan(
            twin,
            detector,
            scorer,
            alert_system,
            "Chain Step 5 - Monitoring Disabled"
        )

        print("\n[CHAINED ATTACK] Sequence complete")

    elif choice == "5":
        from digital_twin.frequency_detector import FrequencyDetector

        freq_detector = FrequencyDetector(twin)

        print("\n[FREQ PROBE] Simulating repeated SSH configuration changes")

        for i in range(4):
            if i % 2 == 0:
                scenario_3_ssh_open(twin)
            else:
                reset_all(twin)

            print(f"  Change {i + 1}: SSH configuration toggled")

        alerts = freq_detector.detect_suspicious_frequency()

        print(f"\n[RESULT] Frequency alerts fired: {len(alerts)}")
if __name__ == "__main__":
    main()