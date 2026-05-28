# UT VPN Azure Resource Monitor

Python | Azure Monitor API | Azure CLI | Ivanti Secure Access | HTML Reporting

University of Tennessee, Knoxville — Azure for Students / Ivanti Secure Access VPN

---

## Background

This project came out of wanting to do something with the infrastructure I
actually have access to as a UT student. I am connected to the UT VPN through
Ivanti Secure Access regularly and I have an Azure for Students subscription
through the university. The question I wanted to answer was whether you could
correlate VPN session activity with cloud resource consumption and surface
anything worth paying attention to.

The tool captures live session metadata from the Ivanti client while connected
to the UT network, pulls real resource metrics from Azure Monitor via the Azure
CLI, aligns the two data streams on a shared timeline, and produces a governance
report showing the relationship between VPN access patterns and Azure resource
utilization.

---

## What It Does

Collects real VPN session data from Ivanti Secure Access including session
duration, bytes in and out, assigned IP, and tunnel type. Authenticates to
the UT Azure for Students subscription and pulls live metrics from Azure Monitor
including ingress, egress, availability, and used capacity. Correlates the two
data streams to identify anomalies where resource activity does not align with
expected VPN session windows. Produces a structured HTML report with session
logs, correlation findings, and flagged anomalies.

---

## Screenshots

### Azure Storage Account Overview
![Azure Storage Overview](screenshots/azure_storage_overview.png)

### Azure Monitor Insights Dashboard
![Azure Insights](screenshots/azure_insights_dashboard.png)

### Azure Metrics Charts
![Azure Metrics](screenshots/azure_metrics_charts.png)

### HTML Correlation Report
![Correlation Report](screenshots/correlation_report.png)

---

## Results

| Metric | Value |
|---|---|
| VPN sessions analyzed | 1 |
| VPN bytes out | 1,545 |
| Azure ingress | 2.5 KiB |
| Azure egress | 3.33 KiB |
| Azure transactions | 28 |
| Average latency | 23.71 ms |
| Anomalies detected | 2 |
| Overall status | Medium |

---

## How to Run

```bash
git clone https://github.com/Damonlee005/UT-VPN-Azure-Resource-Monitor
cd UT-VPN-Azure-Resource-Monitor
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
az login
python scripts/vpn_collector.py
python scripts/azure_monitor.py
python scripts/correlator.py
python scripts/report_generator.py
open reports/correlation_report.html
```

---

## Requirements

- Connected to UT VPN via Ivanti Secure Access
- Azure CLI installed and authenticated to UT Azure for Students subscription
- Python 3.9 or higher

---

## Project Structure
---

## What Makes This Different

Most infrastructure monitoring projects use synthetic data or public datasets.
This one uses real session data from a live university VPN connection and real
resource metrics from an authenticated Azure subscription. Every data point in
the report came from an actual API call to Azure Monitor or an actual Ivanti
session while connected to the UT network.
