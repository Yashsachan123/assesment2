"""
DoS Detection and Prevention System - Main Detection Server
Monitors traffic, detects attack patterns, and blocks malicious IPs
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import time
import os

app = Flask(__name__)

# Configuration
REQUEST_THRESHOLD = 20  # Maximum requests per minute
BLOCK_DURATION = 300  # Block duration in seconds (5 minutes)
MONITOR_WINDOW = 60  # Time window for counting requests (seconds)

# Data structures for tracking
request_tracker = defaultdict(list)  # IP -> list of request timestamps
blocked_ips = {}  # IP -> block expiry time
attack_log = []  # List of attack events
traffic_history = []  # For chart visualization

# Lock for thread-safe operations
data_lock = threading.Lock()


def log_attack(ip_address, request_count):
    """Log attack to file and memory"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] ALERT: {ip_address} exceeded threshold with {request_count} requests - BLOCKED for {BLOCK_DURATION}s\n"
    
    # Write to file
    log_file_path = os.path.join('logs', 'attack_log.txt')
    with open(log_file_path, 'a') as f:
        f.write(log_entry)
    
    # Store in memory for dashboard
    attack_log.append({
        'timestamp': timestamp,
        'ip': ip_address,
        'count': request_count,
        'status': 'BLOCKED'
    })
    
    # Keep only last 50 entries
    if len(attack_log) > 50:
        attack_log.pop(0)


def cleanup_old_requests():
    """Remove old request timestamps and unblock expired IPs"""
    while True:
        time.sleep(10)  # Run every 10 seconds
        
        with data_lock:
            current_time = datetime.now()
            
            # Clean up old request timestamps
            for ip in list(request_tracker.keys()):
                request_tracker[ip] = [
                    ts for ts in request_tracker[ip]
                    if (current_time - ts).total_seconds() < MONITOR_WINDOW
                ]
                if not request_tracker[ip]:
                    del request_tracker[ip]
            
            # Unblock expired IPs
            for ip in list(blocked_ips.keys()):
                if current_time >= blocked_ips[ip]:
                    del blocked_ips[ip]
                    print(f"[{current_time.strftime('%H:%M:%S')}] INFO: {ip} unblocked")


def check_request(ip_address):
    """Check if request should be allowed and update tracking"""
    with data_lock:
        current_time = datetime.now()
        
        # Check if IP is blocked
        if ip_address in blocked_ips:
            if current_time < blocked_ips[ip_address]:
                return False, "IP is blocked"
            else:
                del blocked_ips[ip_address]
        
        # Add current request timestamp
        request_tracker[ip_address].append(current_time)
        
        # Remove old timestamps
        request_tracker[ip_address] = [
            ts for ts in request_tracker[ip_address]
            if (current_time - ts).total_seconds() < MONITOR_WINDOW
        ]
        
        # Check if threshold exceeded
        request_count = len(request_tracker[ip_address])
        
        if request_count > REQUEST_THRESHOLD:
            # Block the IP
            blocked_ips[ip_address] = current_time + timedelta(seconds=BLOCK_DURATION)
            log_attack(ip_address, request_count)
            print(f"[{current_time.strftime('%H:%M:%S')}] ⚠️ ALERT: {ip_address} blocked - {request_count} requests")
            return False, f"Rate limit exceeded: {request_count} requests"
        
        return True, "OK"


def update_traffic_history():
    """Update traffic statistics for visualization"""
    while True:
        time.sleep(5)  # Update every 5 seconds
        
        with data_lock:
            current_time = datetime.now()
            total_requests = sum(len(timestamps) for timestamps in request_tracker.values())
            
            traffic_history.append({
                'time': current_time.strftime("%H:%M:%S"),
                'requests': total_requests,
                'blocked_ips': len(blocked_ips)
            })
            
            # Keep only last 20 data points
            if len(traffic_history) > 20:
                traffic_history.pop(0)


@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/stats')
def get_stats():
    """API endpoint for real-time statistics"""
    with data_lock:
        # Get current request counts per IP
        ip_stats = []
        for ip, timestamps in request_tracker.items():
            ip_stats.append({
                'ip': ip,
                'count': len(timestamps),
                'status': 'BLOCKED' if ip in blocked_ips else 'ACTIVE',
                'last_seen': timestamps[-1].strftime("%H:%M:%S") if timestamps else 'N/A'
            })
        
        # Sort by request count (descending)
        ip_stats.sort(key=lambda x: x['count'], reverse=True)
        
        return jsonify({
            'ip_stats': ip_stats,
            'blocked_ips': [
                {
                    'ip': ip,
                    'unblock_time': expiry.strftime("%H:%M:%S")
                }
                for ip, expiry in blocked_ips.items()
            ],
            'attack_log': attack_log[-10:],  # Last 10 attacks
            'traffic_history': traffic_history,
            'total_requests': sum(len(ts) for ts in request_tracker.values()),
            'total_blocked': len(blocked_ips)
        })


@app.route('/api/simulate_request')
def simulate_request():
    """Simulate a request to test the system"""
    client_ip = request.remote_addr
    allowed, message = check_request(client_ip)
    
    return jsonify({
        'allowed': allowed,
        'message': message,
        'ip': client_ip
    })


@app.route('/api/clear_logs')
def clear_logs():
    """Clear all logs and reset tracking"""
    with data_lock:
        request_tracker.clear()
        blocked_ips.clear()
        attack_log.clear()
        traffic_history.clear()
        
        # Clear log file
        log_file_path = os.path.join('logs', 'attack_log.txt')
        with open(log_file_path, 'w') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Logs cleared\n")
    
    return jsonify({'status': 'success', 'message': 'All logs cleared'})


if __name__ == '__main__':
    print("=" * 60)
    print("DoS Detection and Prevention System - Detection Server")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  - Request Threshold: {REQUEST_THRESHOLD} requests per minute")
    print(f"  - Block Duration: {BLOCK_DURATION} seconds")
    print(f"  - Monitor Window: {MONITOR_WINDOW} seconds")
    print("=" * 60)
    print(f"Dashboard: http://127.0.0.1:8000")
    print("=" * 60)
    
    # Start background threads
    cleanup_thread = threading.Thread(target=cleanup_old_requests, daemon=True)
    cleanup_thread.start()
    
    traffic_thread = threading.Thread(target=update_traffic_history, daemon=True)
    traffic_thread.start()
    
    # Run Flask app
    app.run(host='127.0.0.1', port=8000, debug=False)
