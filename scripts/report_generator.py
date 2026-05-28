import json
import os
from datetime import datetime

def generate_report(correlation_path, output_path):
    with open(correlation_path, 'r') as f:
        data = json.load(f)

    anomaly_count = len(data.get('anomalies', []))
    if anomaly_count >= 2:
        risk_color = '#E65100'
        risk_label = 'MEDIUM'
    elif anomaly_count == 1:
        risk_color = '#F9A825'
        risk_label = 'LOW'
    else:
        risk_color = '#2E7D32'
        risk_label = 'NORMAL'

    session_rows = ''
    for s in data.get('session_summaries', []):
        session_rows += (
            '<tr>'
            '<td>' + s.get('timestamp', '')[:19] + '</td>'
            '<td>' + str(s.get('duration_seconds', 0)) + 's</td>'
            '<td>' + str(s.get('bytes_in', 0)) + '</td>'
            '<td>' + str(s.get('bytes_out', 0)) + '</td>'
            '<td>' + s.get('assigned_ip', '') + '</td>'
            '<td>' + s.get('tunnel_type', '') + ' / ' + s.get('vpn_type', '') + '</td>'
            '</tr>'
        )

    anomaly_rows = ''
    for a in data.get('anomalies', []):
        sev_color = '#C62828' if a['severity'] == 'High' else '#E65100' if a['severity'] == 'Medium' else '#F9A825'
        anomaly_rows += (
            '<tr>'
            '<td>' + a['type'] + '</td>'
            '<td style="color:' + sev_color + ';font-weight:bold">' + a['severity'] + '</td>'
            '<td>' + a['description'] + '</td>'
            '<td>' + a['recommendation'] + '</td>'
            '</tr>'
        )

    findings_rows = ''
    for f in data.get('correlation_findings', []):
        findings_rows += (
            '<tr>'
            '<td>' + f['finding'] + '</td>'
            '<td>' + f['description'] + '</td>'
            '</tr>'
        )

    totals = data.get('totals', {})

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>UT VPN Azure Resource Correlation Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; color: #212121; }
        .header { background: #FF8200; color: white; padding: 30px; border-radius: 8px; margin-bottom: 24px; }
        .header h1 { margin: 0 0 6px 0; font-size: 22px; }
        .header p { margin: 0; opacity: 0.7; font-size: 12px; }
        .badge { display: inline-block; background: ''' + risk_color + '''; color: white; padding: 6px 16px; border-radius: 4px; font-weight: bold; font-size: 13px; margin-top: 10px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
        .card { background: white; padding: 18px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
        .card h3 { margin: 0 0 4px 0; font-size: 12px; color: #757575; text-transform: uppercase; }
        .card .value { font-size: 26px; font-weight: bold; color: white; }
        .section { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); margin-bottom: 24px; }
        .section h2 { margin: 0 0 16px 0; font-size: 15px; border-bottom: 2px solid #e0e0e0; padding-bottom: 8px; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #FF8200; color: #212121; padding: 10px 12px; text-align: left; font-size: 12px; }
        td { padding: 10px 12px; border-bottom: 1px solid #e0e0e0; font-size: 12px; }
        tr:hover td { background: #f5f5f5; }
        .footer { text-align: center; color: #9e9e9e; font-size: 11px; margin-top: 24px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>UT VPN and Azure Resource Correlation Report</h1>
        <p>Generated: ''' + datetime.now().strftime('%B %d, %Y at %I:%M %p') + ''' | University of Tennessee, Knoxville | Azure for Students</p>
        <div class="badge">Status: ''' + risk_label + '''</div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>VPN Sessions</h3>
            <div class="value">''' + str(data.get('vpn_sessions_analyzed', 0)) + '''</div>
        </div>
        <div class="card">
            <h3>VPN Bytes Out</h3>
            <div class="value">''' + str(totals.get('total_vpn_bytes_out', 0)) + '''</div>
        </div>
        <div class="card">
            <h3>Azure Ingress</h3>
            <div class="value">''' + str(totals.get('total_azure_ingress', 0)) + '''</div>
        </div>
        <div class="card">
            <h3>Anomalies</h3>
            <div class="value">''' + str(anomaly_count) + '''</div>
        </div>
    </div>

    <div class="section">
        <h2>VPN Session Log</h2>
        <table>
            <tr><th>Timestamp</th><th>Duration</th><th>Bytes In</th><th>Bytes Out</th><th>Assigned IP</th><th>Tunnel / Type</th></tr>
            ''' + session_rows + '''
        </table>
    </div>

    <div class="section">
        <h2>Correlation Findings</h2>
        <table>
            <tr><th>Finding</th><th>Description</th></tr>
            ''' + findings_rows + '''
        </table>
    </div>

    <div class="section">
        <h2>Anomalies Detected</h2>
        <table>
            <tr><th>Type</th><th>Severity</th><th>Description</th><th>Recommendation</th></tr>
            ''' + anomaly_rows + '''
        </table>
    </div>

    <div class="footer">
        UT VPN Azure Resource Monitor | University of Tennessee, Knoxville | Azure for Students Subscription
    </div>
</body>
</html>'''

    os.makedirs('reports', exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(html)

    print("Report saved to " + output_path)

if __name__ == "__main__":
    generate_report(
        'data/correlation_results.json',
        'reports/correlation_report.html'
    )
