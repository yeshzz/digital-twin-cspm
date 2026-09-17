import json
import os
from datetime import datetime

class DigitalTwin:
    def __init__(self):
        self.resources = {}
        self.baselines = {}
        self.history = []
        self.change_log = {}
        self.load_baselines()
        print("[DIGITAL TWIN] Initialized successfully")

    def load_baselines(self):
        baseline_dir = os.path.join(os.path.dirname(__file__), '..', 'baselines')
        for filename in os.listdir(baseline_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(baseline_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    self.baselines[data['resource_type']] = data['parameters']
        print(f"[DIGITAL TWIN] Loaded {len(self.baselines)} baseline configurations")

    def add_resource(self, resource_id, resource_type, current_config):
        self.resources[resource_id] = {
            "resource_type": resource_type,
            "config": current_config,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        print(f"[DIGITAL TWIN] Resource added: {resource_id} ({resource_type})")

    def update_resource(self, resource_id, new_config):
     if resource_id in self.resources:
        old_config = self.resources[resource_id]["config"].copy()

        # Keep the existing configuration
        updated_config = old_config.copy()

        # Track every parameter that actually changes
        now = datetime.now()

        for param, new_value in new_config.items():
            old_value = old_config.get(param)

            if old_value != new_value:
                key = f"{resource_id}:{param}"

                if key not in self.change_log:
                    self.change_log[key] = []

                self.change_log[key].append(now.timestamp())

        # Update only the parameters provided
        updated_config.update(new_config)

        self.resources[resource_id]["config"] = updated_config
        self.resources[resource_id]["last_updated"] = now.strftime("%Y-%m-%d %H:%M:%S")

        self.history.append({
            "resource_id": resource_id,
            "old_config": old_config,
            "new_config": updated_config,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"[DIGITAL TWIN] Resource updated: {resource_id}")
    def get_all_resources(self):
        return self.resources

    def get_baselines(self):
        return self.baselines

    def get_history(self):
        return self.history
    
    def get_change_log(self):
        return self.change_log
