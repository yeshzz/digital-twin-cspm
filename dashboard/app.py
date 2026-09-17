from flask import Flask, render_template, jsonify, request
from datetime import datetime

def create_app(twin, detector, scorer, alert_system):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/api/scan')
    def scan():
        drifts = detector.detect_drift()
        score = scorer.calculate_posture_score(drifts)
        risk_level = scorer.get_risk_level(score)
        severity_summary = scorer.get_severity_summary(drifts)
        alerts = alert_system.generate_alerts(drifts)

        return jsonify({
            "score": score,
            "risk_level": risk_level,
            "score_color": scorer.get_score_color(score),
            "total_resources": len(twin.get_all_resources()),
            "total_drifts": len(drifts),
            "severity_summary": severity_summary,
            "drifts": drifts,
            "alerts": alerts,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    @app.route('/api/simulate/<int:scenario_id>')
    def simulate(scenario_id):
        import sys, os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from simulations.attack_scenarios import (
            scenario_1_public_s3, scenario_2_admin_iam,
            scenario_3_ssh_open, scenario_4_encryption_disabled,
            scenario_5_monitoring_off, reset_all
        )
        scenarios = {
            1: scenario_1_public_s3,
            2: scenario_2_admin_iam,
            3: scenario_3_ssh_open,
            4: scenario_4_encryption_disabled,
            5: scenario_5_monitoring_off
        }
        if scenario_id == 0:
            reset_all(twin)
            return jsonify({"message": "Reset to secure baseline"})
        elif scenario_id in scenarios:
            scenarios[scenario_id](twin)
            return jsonify({"message": f"Scenario {scenario_id} applied"})
        return jsonify({"error": "Invalid scenario"})

    @app.route('/api/resources')
    def resources():
        return jsonify(twin.get_all_resources())

    @app.route('/api/alerts')
    def alerts():
        return jsonify(alert_system.get_all_alerts())

    return app
