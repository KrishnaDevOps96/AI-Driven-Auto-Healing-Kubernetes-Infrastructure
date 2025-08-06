import requests
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import datetime
from kubernetes import client, config

PROMETHEUS_URL = "http://localhost:9090"

# Query CPU usage from Prometheus
def query_prometheus(metric, duration="5m"):
    query = f'{metric}[{duration}]'
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": query})
    return response.json()

# Extract metric values from Prometheus response
def extract_values(prom_data):
    values = []
    for result in prom_data['data']['result']:
        for val in result['values']:
            timestamp, metric_value = val
            values.append([float(metric_value)])
    return values

# Use Isolation Forest to detect anomalies
def detect_anomaly(data):
    df = pd.DataFrame(data, columns=["value"])
    model = IsolationForest(contamination=0.1)
    df['anomaly'] = model.fit_predict(df[["value"]])
    anomalies = df[df['anomaly'] == -1]
    return anomalies

# Restart target pod (example: nginx)
def restart_pod(namespace="default"):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)
    target_pod = None

    for pod in pods.items:
        if "nginx" in pod.metadata.name:  # Customize pod name condition
            target_pod = pod.metadata.name
            break

    if target_pod:
        print(f"🔄 Restarting pod: {target_pod}")
        v1.delete_namespaced_pod(name=target_pod, namespace=namespace)
    else:
        print("❗ No matching pod found to restart.")

# Main script
def main():
    metric = "container_cpu_usage_seconds_total"  # Customize as needed
    data = query_prometheus(metric)
    values = extract_values(data)

    if not values:
        print("⚠️ No data received from Prometheus.")
        return

    anomalies = detect_anomaly(values)

    if not anomalies.empty:
        print(f"[{datetime.now()}] 🚨 Anomaly Detected:")
        print(anomalies)
        restart_pod()
    else:
        print(f"[{datetime.now()}] ✅ All normal.")

# Entry point
if __name__ == "__main__":
    main()
