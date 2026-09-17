# Digital Twin — Cloud Security Posture & Drift Detection

**IIIT Trichy Funded Research Project**
**Researcher:** Yashaswini C | T. John Institute of Technology, Bengaluru

## What This Project Does
A Digital Twin system that mirrors cloud infrastructure configurations in real time, detects security misconfigurations (drift), scores overall security posture, and fires alerts for critical deviations.

## How To Run

### Install dependencies
pip install -r requirements.txt

### Run the project
python main.py

### Choose option:
- 1: Run all 5 attack scenarios automatically
- 2: Run individual scenario
- 3: Launch web dashboard at http://localhost:5000

## Project Structure
- digital_twin/ — Core digital twin engine
- baselines/ — Secure baseline JSON configurations
- simulations/ — Attack scenario simulations
- dashboard/ — Flask web dashboard
- templates/ — HTML frontend
- static/ — CSS styling

## Attack Scenarios
1. S3 Bucket Public Exposure (Critical)
2. IAM Admin Access Granted (Critical)
3. SSH Open to All IPs (High)
4. Encryption Disabled (Critical)
5. Monitoring Disabled (Medium)
