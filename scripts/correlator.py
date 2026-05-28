import json
import os
from datetime import datetime

def load_vpn_sessions():
    with open('data/vpn_sessions.json', 'r') as f:
        return json.load(f)

def load_azure_metrics():
    with open('data/azure_metrics.json', 'r') as f:
        return json.load(f)

def parse_duration(duration_str):
    try:
        total_seconds = 0
        parts = duration_str.replace('python scripts/vpn_collector.py', '').strip()
        if 'h' in parts:
            h, rest = parts.split('h')
            total_seconds += int(h.strip()) * 3600
            parts = rest
        if 'm' in parts:
            m, rest = parts.split('m')
            total_seconds += int(m.strip()) * 60
            parts = rest
        if 's' in parts:
            s = parts.replace('s', '').strip()
            if s:
                total_seconds += int(s)
        return total_seconds
    except:
        return 0

def correlate(sessions, metrics):
    results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'vpn_sessions_analyzed': len(sessions),
        'azure_resource': metrics['resource'],
        'subscription': metrics['subscription'],
        'session_summaries': [],
        'correlation_findings': [],
        'anomalies': []
    }

    total_bytes_in = 0
    total_bytes_out = 0

    for session in sessions:
        try:
            bytes_in = int(session.get('bytes_in', 0))
            bytes_out = int(session.get('bytes_out', 0))
        except:
            bytes_in = 0
            bytes_out = 0

        total_bytes_in += bytes_in
        total_bytes_out += bytes_out
        duration_seconds = parse_duration(session.get('session_duration', '0s'))

        summary = {
            'timestamp': session['timestamp'],
            'duration_seconds': duration_seconds,
            'bytes_in': bytes_in,
            'bytes_out': bytes_out,
            'assigned_ip': session.get('assigned_ip', 'unknown'),
            'tunnel_type': session.get('tunnel_type', 'unknown'),
            'vpn_type': session.get('vpn_type', 'unknown')
        }
        results['session_summaries'].append(summary)

    ingress_points = metrics['metrics'].get('Ingress', [])
    egress_points = metrics['metrics'].get('Egress', [])

    total_azure_ingress = sum(p['value'] for p in ingress_points)
    total_azure_egress = sum(p['value'] for p in egress_points)

    results['correlation_findings'] = [
        {
            'finding': 'VPN to Azure Ingress Ratio',
            'vpn_bytes_out': total_bytes_out,
            'azure_ingress_bytes': total_azure_ingress,
            'description': 'Compares bytes leaving VPN client against bytes entering Azure storage'
        },
        {
            'finding': 'Session Activity Window',
            'sessions_recorded': len(sessions),
            'azure_data_points': len(ingress_points),
            'description': 'VPN sessions logged against Azure metric collection windows'
        }
    ]

    if total_bytes_out > 0 and total_azure_ingress == 0:
        results['anomalies'].append({
            'type': 'Resource Activity Without VPN Correlation',
            'severity': 'Medium',
            'description': 'Azure resource shows no ingress during active VPN session window',
            'recommendation': 'Verify resource access controls and review network routing'
        })

    if total_bytes_in == 0 and total_bytes_out > 0:
        results['anomalies'].append({
            'type': 'One-Directional VPN Traffic',
            'severity': 'Low',
            'description': 'VPN session shows outbound traffic only with no inbound data',
            'recommendation': 'Normal for initial connection setup but monitor for extended periods'
        })

    results['totals'] = {
        'total_vpn_bytes_in': total_bytes_in,
        'total_vpn_bytes_out': total_bytes_out,
        'total_azure_ingress': total_azure_ingress,
        'total_azure_egress': total_azure_egress
    }

    os.makedirs('data', exist_ok=True)
    with open('data/correlation_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("Correlation analysis complete")
    print("VPN sessions analyzed: " + str(len(sessions)))
    print("Azure ingress total: " + str(total_azure_ingress) + " bytes")
    print("Azure egress total: " + str(total_azure_egress) + " bytes")
    print("Anomalies detected: " + str(len(results['anomalies'])))

    return results

if __name__ == "__main__":
    sessions = load_vpn_sessions()
    metrics = load_azure_metrics()
    correlate(sessions, metrics)
    print("\nResults saved to data/correlation_results.json")
