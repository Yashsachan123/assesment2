# DoS Detection and Prevention System - Setup Guide

## 📋 Project Overview

This is a **Localhost DoS (Denial of Service) Attack Detection and Prevention System** built with Python Flask. The system monitors network traffic, detects suspicious patterns, and automatically blocks malicious IP addresses.

---

## 🏗️ Project Structure

```
/vercel/sandbox/
├── app.py                      # Main detection server (Port 8000)
├── target_server.py            # Simulated victim server (Port 5000)
├── attack_simulator.py         # Attack testing tool
├── requirements.txt            # Python dependencies
├── templates/
│   └── dashboard.html          # Web dashboard interface
├── static/
│   ├── css/
│   │   └── style.css          # Dashboard styling
│   └── js/
│       └── dashboard.js       # Real-time updates & charts
└── logs/
    └── attack_log.txt         # Attack records
```

---

## ⚙️ System Configuration

### Detection Parameters:
- **Request Threshold:** 20 requests per minute
- **Block Duration:** 5 minutes (300 seconds)
- **Monitor Window:** 60 seconds
- **Auto-refresh:** Every 3 seconds

---

## 🚀 Installation Steps

### Step 1: Install Python
Make sure Python 3.10 or 3.11 is installed:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Requests 2.31.0
- Werkzeug 3.0.1

### Step 3: Verify Installation
```bash
python -c "import flask; import requests; print('✅ All dependencies installed')"
```

---

## 🎯 How to Run the System

### Method 1: Run All Components Separately

#### Terminal 1 - Start Target Server (Victim):
```bash
python target_server.py
```
- Runs on: http://127.0.0.1:5000
- This is the simulated website that will be "attacked"

#### Terminal 2 - Start Detection Server:
```bash
python app.py
```
- Runs on: http://127.0.0.1:8000
- Open dashboard: http://127.0.0.1:8000

#### Terminal 3 - Run Attack Simulator (Optional):
```bash
python attack_simulator.py
```
- Interactive menu to simulate different attack types

---

## 🖥️ Using the Dashboard

### Access the Dashboard:
Open your browser and go to: **http://127.0.0.1:8000**

### Dashboard Features:

1. **Header Stats**
   - Total Requests: Current active requests
   - Blocked IPs: Number of blocked IP addresses

2. **Traffic Monitor Chart**
   - Real-time line chart showing request trends
   - Blue line: Total requests
   - Red line: Blocked IPs

3. **Active IP Addresses Table**
   - Shows all active IPs
   - Request count per IP
   - Status (ACTIVE/BLOCKED)
   - Last seen timestamp

4. **System Configuration**
   - Current detection settings
   - Target server URL

5. **Blocked IP Addresses**
   - List of currently blocked IPs
   - Unblock time for each IP

6. **Recent Attack Log**
   - Chronological list of detected attacks
   - Timestamp, IP, request count

7. **Test Controls**
   - "Send Test Request" button to test the system
   - "Clear Logs" button to reset all data

---

## 🧪 Testing the System

### Test 1: Normal Traffic (Should NOT trigger detection)
```bash
python attack_simulator.py
# Select option 1
# Duration: 30 seconds
# Rate: 1 request per second
```
**Expected Result:** All requests succeed, no blocking

### Test 2: DoS Attack (Should trigger detection)
```bash
python attack_simulator.py
# Select option 2
# Total requests: 50
# Delay: 0.1 seconds
```
**Expected Result:** IP gets blocked after ~20 requests

### Test 3: Distributed Attack
```bash
python attack_simulator.py
# Select option 3
# Total requests: 100
# Threads: 5
```
**Expected Result:** Rapid blocking due to high request rate

### Test 4: Manual Testing
1. Open dashboard: http://127.0.0.1:8000
2. Click "Send Test Request" button multiple times rapidly
3. After 20+ clicks, you should see:
   - Alert banner appears
   - Your IP appears in blocked list
   - Attack logged in the log section

---

## 📊 Understanding the Detection Logic

### How Detection Works:

1. **Request Tracking:**
   - Every request is logged with timestamp and IP
   - System tracks requests in a 60-second window

2. **Threshold Check:**
   - If IP exceeds 20 requests in 60 seconds → BLOCKED
   - Block duration: 5 minutes

3. **Auto-Unblock:**
   - After 5 minutes, IP is automatically unblocked
   - Background thread cleans up old data every 10 seconds

4. **Logging:**
   - All attacks logged to `logs/attack_log.txt`
   - Dashboard shows last 10 attacks

---

## 📝 Log File Format

Location: `logs/attack_log.txt`

Format:
```
[2025-11-01 12:30:45] ALERT: 127.0.0.1 exceeded threshold with 25 requests - BLOCKED for 300s
[2025-11-01 12:35:20] ALERT: 192.168.1.100 exceeded threshold with 30 requests - BLOCKED for 300s
```

---

## 🔧 Customization

### Change Detection Parameters:

Edit `app.py`:
```python
REQUEST_THRESHOLD = 20      # Change to 30 for higher threshold
BLOCK_DURATION = 300        # Change to 600 for 10-minute blocks
MONITOR_WINDOW = 60         # Change to 120 for 2-minute window
```

### Change Ports:

**Detection Server (app.py):**
```python
app.run(host='127.0.0.1', port=8000, debug=False)
```

**Target Server (target_server.py):**
```python
app.run(host='127.0.0.1', port=5000, debug=False)
```

---

## 🐛 Troubleshooting

### Problem: "Port already in use"
**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### Problem: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Problem: Dashboard not updating
**Solution:**
- Hard refresh browser: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- Check browser console for JavaScript errors
- Ensure detection server is running

### Problem: Target server not responding
**Solution:**
- Verify target_server.py is running
- Check http://127.0.0.1:5000 in browser
- Look for error messages in terminal

---

## 📚 API Endpoints

### Detection Server (Port 8000):

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard page |
| `/api/stats` | GET | Get real-time statistics (JSON) |
| `/api/simulate_request` | GET | Simulate a test request |
| `/api/clear_logs` | GET | Clear all logs and reset tracking |

### Target Server (Port 5000):

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/about` | GET | About page |
| `/api/data` | GET | API endpoint (JSON) |
| `/reset` | GET | Reset request counter |

---

## 🎓 For Presentation/Viva

### Key Points to Highlight:

1. **Real-time Monitoring:** Dashboard updates every 3 seconds
2. **Automatic Detection:** No manual intervention needed
3. **Visual Feedback:** Charts and alerts for easy understanding
4. **Configurable:** Easy to adjust thresholds and parameters
5. **Logging:** Persistent attack records for analysis
6. **Testing Tools:** Built-in simulator for demonstration

### Demo Flow:
1. Show both servers running
2. Open dashboard and explain features
3. Run normal traffic test (no blocking)
4. Run DoS attack simulation (show blocking)
5. Show logs and blocked IPs
6. Demonstrate auto-unblock after timeout

---

## 📄 License

This project is for educational and testing purposes only.

---

## 👨‍💻 Author

Created as part of Assignment 2 for learning and testing purposes.

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments in each file
3. Test with the attack simulator first
4. Verify all dependencies are installed

---

**Happy Testing! 🚀**
