class RiskScorer:
    def __init__(self):
        self.severity_weights = {
            "CRITICAL": 25,
            "HIGH": 15,
            "MEDIUM": 8,
            "LOW": 3
        }
        print("[RISK SCORER] Initialized successfully")

    def calculate_posture_score(self, drifts):
        if not drifts:
            return 100

        total_penalty = 0
        for drift in drifts:
            severity = drift.get("severity", "LOW")
            total_penalty += self.severity_weights.get(severity, 3)

        score = max(0, 100 - total_penalty)
        return score

    def get_risk_level(self, score):
        if score >= 80:
            return "SECURE"
        elif score >= 60:
            return "MODERATE"
        elif score >= 40:
            return "HIGH RISK"
        else:
            return "CRITICAL RISK"

    def get_score_color(self, score):
        if score >= 80:
            return "green"
        elif score >= 60:
            return "orange"
        else:
            return "red"

    def get_severity_summary(self, drifts):
        summary = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for drift in drifts:
            severity = drift.get("severity", "LOW")
            summary[severity] += 1
        return summary
