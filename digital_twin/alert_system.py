from datetime import datetime


class AlertSystem:
    def __init__(self):
        self.alerts = []
        print("[ALERT SYSTEM] Initialized successfully")

    def generate_alerts(self, drifts):
        new_alerts = []

        # Prevent duplicate alerts for the same active drift
        existing_keys = {
            (alert["resource_id"], alert["parameter"])
            for alert in self.alerts
            if alert["status"] == "OPEN"
        }

        for drift in drifts:
            if drift["severity"] in ["CRITICAL", "HIGH"]:

                key = (drift["resource_id"], drift["parameter"])

                # Skip if this drift already has an open alert
                if key in existing_keys:
                    continue

                alert = {
                    "alert_id": f"ALERT-{len(self.alerts) + 1:03d}",
                    "severity": drift["severity"],
                    "resource_id": drift["resource_id"],
                    "resource_type": drift["resource_type"],
                    "message": f"{drift['severity']} drift detected on {drift['resource_id']}",
                    "parameter": drift["parameter"],
                    "expected": drift["expected"],
                    "found": drift["found"],
                    "remediation": drift["remediation"],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "OPEN"
                }

                new_alerts.append(alert)
                self.alerts.append(alert)
                existing_keys.add(key)

                print(
                    f"[ALERT FIRED] {alert['alert_id']} - {alert['message']}"
                )

        return new_alerts

    def get_all_alerts(self):
        return self.alerts

    def get_open_alerts(self):
        return [
            alert for alert in self.alerts
            if alert["status"] == "OPEN"
        ]