# UT VPN Azure Resource Monitor

Python | Azure Monitor API | Azure CLI | Ivanti Secure Access | HTML Reporting

University of Tennessee, Knoxville — Azure for Students / Ivanti Secure Access

---

## Why I Built This

As a UT student I have two things most people building projects do not have
access to, a live university VPN connection through Ivanti Secure Access and
an Azure for Students subscription tied to the UT tenant. I wanted to actually
use both of them for something meaningful instead of just connecting to the VPN
to access campus resources and forgetting it existed.

The question that drove this project was simple. When I connect to the UT VPN
and interact with Azure resources, what does that activity actually look like
at the infrastructure level and can you surface anything worth paying attention
to by correlating the two data streams. 

Academically this project pushed me to work with real enterprise APIs and
cloud infrastructure that I only had conceptaul knowledge of. Technically I wanted to
learn how Azure Monitor works, how to authenticate and query it programmatically,
and how to take two separate live data sources and make them talk to each other
in a way that produces something useful.

---

## What It Does

Captures live VPN session metadata from Ivanti Secure Access while connected
to the UT network including session duration, bytes transferred, assigned IP,
and tunnel configuration. Authenticates to the UT Azure for Students subscription
using the Azure CLI and pulls real resource metrics from Azure Monitor including
ingress, egress, availability, and transaction counts. Correlates the two data
streams on a shared timeline to identify anomalies where cloud resource activity
does not align with expected VPN session windows. Produces an HTML governance
report with session logs, correlation findings, and flagged anomalies.

---

## Screenshots

### Azure Storage Account Overview

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

## What I Learned

Working with the Azure Monitor API was the biggest technical lift. The
authentication flow through the Azure CLI, scoping API calls to specific
resources, and parsing the metric response format all took more time than
I expected. The correlation logic was conceptually straightforward but
getting the two data streams aligned on a shared timeline required thinking
carefully about how VPN session timestamps and Azure metric collection
windows relate to each other.

The bigger takeaway was understanding what enterprise infrastructure monitoring
actually looks like in practice. This is a small scale version of what IT
operations teams do across thousands of resources. Building even a simple
version of it made the operational side of IT feel a lot more concrete than
it did from a textbook.

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
UT-VPN-Azure-Resource-Monitor/
├── scripts/
│   ├── vpn_collector.py
│   ├── azure_monitor.py
│   ├── correlator.py
│   └── report_generator.py
├── data/
├── reports/
├── screenshots/
└── requirements.txt
