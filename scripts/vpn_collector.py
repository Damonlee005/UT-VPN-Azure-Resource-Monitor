import json
import os
from datetime import datetime

def collect_vpn_session():
    """
    Collects current VPN session data from Ivanti Secure Access.
    Run this while connected to UT VPN.
    """
    print("Enter your current Ivanti VPN session data.")
    print("Open Ivanti Secure Access client and copy the values.\n")

    session = {
        'timestamp': datetime.now().isoformat(),
        'session_duration': input("Session duration (e.g. 31m 48s): "),
        'bytes_in': input("Bytes in: "),
        'bytes_out': input("Bytes out: "),
        'assigned_ip': input("Assigned IPv4: "),
        'tunnel_type': input("Tunnel type (e.g. VPN): "),
        'vpn_type': input("VPN type (e.g. ESP): "),
        'connection_source': input("Connection source: "),
        'status': 'connected'
    }

    os.makedirs('data', exist_ok=True)
    sessions_file = 'data/vpn_sessions.json'

    sessions = []
    if os.path.exists(sessions_file):
        with open(sessions_file, 'r') as f:
            sessions = json.load(f)

    sessions.append(session)

    with open(sessions_file, 'w') as f:
        json.dump(sessions, f, indent=2)

    print("\nVPN session logged successfully.")
    print("Session timestamp: " + session['timestamp'])
    print("Bytes in: " + session['bytes_in'])
    print("Bytes out: " + session['bytes_out'])

    return session

if __name__ == "__main__":
    collect_vpn_session()
