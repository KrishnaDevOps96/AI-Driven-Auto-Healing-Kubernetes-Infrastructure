# 🤖 AI-Driven Auto-Healing Kubernetes Infrastructure

## 📌 Project Overview

An AI-powered Kubernetes infrastructure that detects anomalies in application metrics using a Python-based ML model and automatically heals the environment by restarting unhealthy pods. Visualized and monitored in real-time via Grafana and Prometheus.

> Built using k3s, Prometheus, Grafana, Kubernetes Python client, and an Isolation Forest ML model.

---

## 🎯 Key Features

* 🔍 **Anomaly Detection**: Uses Prometheus metrics and a Python ML model (Isolation Forest) to detect abnormal behavior in pods.
* 🔁 **Auto-Healing**: Automatically restarts Kubernetes pods when anomalies are detected.
* 📊 **Monitoring**: Integrated Grafana dashboards for CPU, memory, and pod restart metrics.
* ⏰ **Scheduled Detection**: Healing service runs as a Kubernetes CronJob every 2 minutes.
* 🐳 **Containerized**: Dockerized and deployed on k3s.

---

## 🧱 Architecture Diagram

```text
+-------------------+             +------------------------+
| Kubernetes Cluster| <---------> |  Prometheus + Grafana  |
+-------------------+             +------------------------+
           |                                 |
           |                                 |
+---------------------------+       +--------------------------+
|   Application Workloads   | <-->  |  Python AI Microservice  |
| (e.g., Nginx, stress pods)|       |  (Anomaly Detection +    |
+---------------------------+       |  Auto-Healing Logic)     |
                                     +--------------------------+
                                                |
                                  [K8s Python Client API]
                                                |
                                 +--------------------------+
                                 |  Auto-Healing Controller |
                                 |  (Pod Restart / Recovery) |
                                 +--------------------------+
```

---

## 🚀 Technologies Used

* **Kubernetes (k3s)**
* **Prometheus + Grafana**
* **Python + scikit-learn** (Isolation Forest)
* **Docker**
* **Helm (for Prometheus install)**
* **Kubernetes Python Client**

---

## 🧪 How It Works

1. Prometheus scrapes pod-level metrics (CPU, memory).
2. Python microservice pulls data via Prometheus HTTP API.
3. AI model detects anomalies based on CPU patterns.
4. On detection, a pod is restarted using the Kubernetes API.
5. Grafana visualizes the metrics and healing actions.

---

## 📦 Project Structure

```
├── anomaly_detector.py         # Core AI logic + K8s auto-healing
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Containerize the script
├── cronjob.yaml                # K8s CronJob definition
├── dashboard_grafana.json      # (Optional) Pre-built Grafana dashboard
└── README.md                   # You're reading it 😄
```

---

## 📷 Screenshots

<img width="2866" height="1562" alt="image" src="https://github.com/user-attachments/assets/8db4426a-fda8-4a2a-8fd4-eb2dae4e0821" />


---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/ai-autohealing-k8s
cd ai-autohealing-k8s
```

### 2. Build Docker Image

```bash
docker build -t ai-healer:latest .
```

### 3. Push Image (if using remote k3s)

```bash
docker tag ai-healer:latest your-dockerhub/ai-healer:latest
docker push your-dockerhub/ai-healer:latest
```

### 4. Deploy Prometheus & Grafana

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm install prom prometheus-community/prometheus --namespace monitoring --create-namespace
helm install grafana grafana/grafana --namespace grafana --create-namespace
```

### 5. Apply CronJob

```bash
kubectl apply -f cronjob.yaml
```

---

## ✅ Sample Prometheus Queries

### CPU Usage by Pod

```promql
sum(rate(container_cpu_usage_seconds_total{container!=""}[2m])) by (pod)
```

### Pod Restart Count

```promql
kube_pod_container_status_restarts_total
```

### Node CPU Total

```promql
sum(rate(node_cpu_seconds_total{mode!="idle"}[1m])) by (instance)
```

---

## 📄 License

MIT

---

## 🧠 Author

**Sai Krishna Bethamcharla**
LinkedIn: [linkedin.com/in/saikrishna-bethamcharla](https://www.linkedin.com/in/saikrishna-bethamcharla)

---

## 💬 Want to Contribute?

Pull requests and feedback are welcome! Fork the repo, create a feature branch, and submit a PR.
