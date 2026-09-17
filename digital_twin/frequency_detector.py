"""
Change Frequency Detection

Detects repeated configuration changes within a time window.
This complements baseline drift detection by identifying
unusually frequent configuration changes.
"""

from datetime import datetime

CHANGE_THRESHOLD = 3
TIME_WINDOW_SECONDS = 3600


class FrequencyDetector:
    def __init__(self, twin):
        self.twin = twin

        print("[FREQUENCY DETECTOR] Initialized")
        print(
            f"[FREQUENCY DETECTOR] Threshold: "
            f"{CHANGE_THRESHOLD} changes per hour"
        )

    def detect_suspicious_frequency(self):
        alerts = []

        now = datetime.now().timestamp()
        change_log = self.twin.get_change_log()

        for key, timestamps in change_log.items():

            recent_changes = [
                timestamp
                for timestamp in timestamps
                if now - timestamp <= TIME_WINDOW_SECONDS
            ]

            if len(recent_changes) >= CHANGE_THRESHOLD:

                resource_id, parameter = key.split(":", 1)

                alert = {
                    "type": "SUSPICIOUS_FREQUENCY",
                    "resource_id": resource_id,
                    "parameter": parameter,
                    "changes_in_window": len(recent_changes),
                    "threshold": CHANGE_THRESHOLD,
                    "severity": "HIGH",
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "message": (
                        f"'{parameter}' on '{resource_id}' changed "
                        f"{len(recent_changes)} times within 1 hour. "
                        f"Threshold: {CHANGE_THRESHOLD}. "
                        f"Possible repeated probing behaviour."
                    )
                }

                alerts.append(alert)

                print(f"[FREQ ALERT] {alert['message']}")

        return alerts