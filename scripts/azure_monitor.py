import json
import os
import subprocess
from datetime import datetime, timedelta

SUBSCRIPTION_ID = "92de2d00-eb95-4fb1-b51a-e53ea5b0c67f"
RESOURCE_GROUP = "vpn-monitor-rg"
STORAGE_ACCOUNT = "utkvpnmonitor"
RESOURCE_ID = (
    "/subscriptions/" + SUBSCRIPTION_ID +
    "/resourceGroups/" + RESOURCE_GROUP +
    "/providers/Microsoft.Storage/storageAccounts/" + STORAGE_ACCOUNT
)

METRICS = ["Ingress", "Egress", "Availability", "UsedCapacity"]

def get_metric(metric_name):
    cmd = [
        "az", "monitor", "metrics", "list",
        "--resource", RESOURCE_ID,
        "--metric", metric_name,
        "--interval", "PT1H",
        "--output", "json"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error fetching " + metric_name + ": " + result.stderr)
        return []

    data = json.loads(result.stdout)
    readings = []
    for item in data.get("value", []):
        for ts in item.get("timeseries", []):
            for point in ts.get("data", []):
                if point.get("total") is not None or point.get("average") is not None:
                    readings.append({
                        "timestamp": point.get("timeStamp"),
                        "metric": metric_name,
                        "value": point.get("total") or point.get("average") or 0
                    })
    return readings

def collect_azure_metrics():
    print("Collecting Azure Monitor metrics for " + STORAGE_ACCOUNT + "...")
    all_metrics = {}

    for metric in METRICS:
        print("  Fetching " + metric + "...")
        readings = get_metric(metric)
        all_metrics[metric] = readings
        print("  Got " + str(len(readings)) + " data points")

    os.makedirs('data', exist_ok=True)
    output = {
        'collected_at': datetime.now().isoformat(),
        'resource': STORAGE_ACCOUNT,
        'subscription': 'Azure for Students - University of Tennessee',
        'metrics': all_metrics
    }

    with open('data/azure_metrics.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\nAzure metrics saved to data/azure_metrics.json")
    return output

if __name__ == "__main__":
    collect_azure_metrics()
