# 🛡️ Localhost DoS Detection and Prevention System

## Project Overview

A comprehensive **Denial of Service (DoS) Attack Detection and Prevention System** built with Python Flask. This system monitors localhost traffic in real-time, detects suspicious patterns, and automatically blocks malicious IP addresses.

### 🎯 Key Features

- ✅ **Real-time Traffic Monitoring** - Live dashboard with auto-refresh
- ✅ **Automatic Attack Detection** - Intelligent rate limiting
- ✅ **IP Blocking System** - Temporary blocks with auto-unblock
- ✅ **Visual Dashboard** - Charts, tables, and alerts
- ✅ **Attack Logging** - Persistent log files
- ✅ **Testing Tools** - Built-in attack simulator
- ✅ **Thread-Safe Operations** - Concurrent request handling
- ✅ **Configurable Parameters** - Easy customization

---

## 📁 Project Structure

```
DoS_Detection_System/
│
├── app.py                      # Main detection server (Port 8000)
│   ├── Request tracking
│   ├── IP blocking logic
│   ├── API endpoints
│   └── Background cleanup threads
│
├── target_server.py            # Simulated victim server (Port 5000)
│   ├── Multiple endpoints
│   ├── Request counter
│   └── Beautiful UI
│
├── attack_simulator.py         # Attack testing tool
│   ├── Normal traffic simulation
│   ├── DoS attack simulation
│   ├── Distributed attack simulation
│   └── Interactive menu
│
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── dashboard.html          # Main dashboard interface
│
├── static/
│   ├── css/
│   │   └── style.css          # Professional styling
│   └── js/
│       └── dashboard.js       # Real-time updates & Chart.js
│
├── logs/
│   └── attack_log.txt         # Attack records
│
├── SETUP_GUIDE.md             # Detailed setup instructions
└── USAGE_INSTRUCTIONS.md      # Quick usage guide
```

---

## 🔧 Technical Specifications

### System Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Request Threshold | 20 requests/min | Maximum allowed requests |
| Block Duration | 5 minutes | How long IPs stay blocked |
| Monitor Window | 60 seconds | Time window for counting |
| Auto-refresh Rate | 3 seconds | Dashboard update frequency |
| Cleanup Interval | 10 seconds | Background cleanup cycle |

### Technology Stack

- **Backend:** Python 3.10+, Flask 3.0.0
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Visualization:** Chart.js 4.4.0
- **HTTP Client:** Requests 2.31.0
- **Threading:** Python threading module

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Target Server
```bash
python target_server.py
```
Server will run at: http://127.0.0.1:5000

### Step 3: Start Detection Server
```bash
python app.py
```
Dashboard will be available at: http://127.0.0.1:8000

### Step 4: Open Dashboard
Navigate to http://127.0.0.1:8000 in your browser

---

## 📊 How It Works

### Detection Algorithm

```
1. Request Received
   ↓
2. Extract IP Address
   ↓
3. Check if IP is Blocked
   ├─ YES → Return 429 (Too Many Requests)
   └─ NO → Continue
       ↓
4. Add Timestamp to Tracker
   ↓
5. Count Requests in Last 60 Seconds
   ↓
6. Check if Count > Threshold (20)
   ├─ YES → Block IP for 5 Minutes
   │        Log Attack
   │        Send Alert
   └─ NO → Allow Request
```

### Data Structures

```python
# Request tracking
request_tracker = {
    '127.0.0.1': [timestamp1, timestamp2, ...],
    '192.168.1.100': [timestamp1, timestamp2, ...]
}

# Blocked IPs
blocked_ips = {
    '127.0.0.1': expiry_datetime,
    '192.168.1.100': expiry_datetime
}

# Attack log
attack_log = [
    {'timestamp': '...', 'ip': '...', 'count': 25, 'status': 'BLOCKED'},
    ...
]
```

---

## 🧪 Testing the System

### Method 1: Dashboard Test Button
1. Open http://127.0.0.1:8000
2. Click "Send Test Request" 25+ times
3. Observe blocking in real-time

### Method 2: Attack Simulator
```bash
python attack_simulator.py
```

**Available Tests:**
- **Normal Traffic:** 1 request/second (should NOT trigger)
- **DoS Attack:** 50 requests with 0.1s delay (should trigger)
- **Distributed Attack:** 100 requests across 5 threads (should trigger)

### Method 3: Manual Browser Testing
1. Open http://127.0.0.1:5000
2. Refresh rapidly 25+ times
3. Check dashboard for blocking

---

## 📈 Dashboard Features

### 1. Header Statistics
- **Total Requests:** Current active request count
- **Blocked IPs:** Number of currently blocked addresses

### 2. Traffic Monitor Chart
- Real-time line chart
- Blue line: Total requests over time
- Red line: Blocked IPs over time
- Updates every 3 seconds

### 3. Active IP Addresses Table
| Column | Description |
|--------|-------------|
| IP Address | Client IP address |
| Requests | Number of requests in window |
| Status | ACTIVE or BLOCKED |
| Last Seen | Timestamp of last request |

### 4. System Configuration
- Current threshold settings
- Block duration
- Monitor window
- Target server URL

### 5. Blocked IP Addresses
- List of currently blocked IPs
- Unblock time for each IP
- Auto-updates as IPs are unblocked

### 6. Recent Attack Log
- Chronological attack history
- Timestamp, IP, request count
- Last 10 attacks displayed

### 7. Test Controls
- **Send Test Request:** Simulate a request
- **Clear Logs:** Reset all tracking data

---

## 🔌 API Endpoints

### Detection Server (Port 8000)

#### GET `/`
Returns the main dashboard HTML page.

#### GET `/api/stats`
Returns real-time statistics in JSON format.

**Response:**
```json
{
  "ip_stats": [
    {"ip": "127.0.0.1", "count": 15, "status": "ACTIVE", "last_seen": "12:30:45"}
  ],
  "blocked_ips": [
    {"ip": "192.168.1.100", "unblock_time": "12:35:00"}
  ],
  "attack_log": [
    {"timestamp": "2025-11-01 12:30:00", "ip": "127.0.0.1", "count": 25, "status": "BLOCKED"}
  ],
  "traffic_history": [
    {"time": "12:30:00", "requests": 10, "blocked_ips": 1}
  ],
  "total_requests": 50,
  "total_blocked": 2
}
```

#### GET `/api/simulate_request`
Simulates a request to test the detection system.

**Response:**
```json
{
  "allowed": true,
  "message": "OK",
  "ip": "127.0.0.1"
}
```

#### GET `/api/clear_logs`
Clears all logs and resets tracking data.

**Response:**
```json
{
  "status": "success",
  "message": "All logs cleared"
}
```

### Target Server (Port 5000)

#### GET `/`
Home page with request counter.

#### GET `/about`
About page with information.

#### GET `/api/data`
API endpoint returning JSON data.

#### GET `/reset`
Resets the request counter.

---

## 🎨 UI/UX Features

### Design Highlights
- **Modern Gradient Background** - Purple to blue gradient
- **Card-Based Layout** - Clean, organized sections
- **Responsive Design** - Works on all screen sizes
- **Real-time Updates** - No manual refresh needed
- **Color-Coded Status** - Green (active), Red (blocked)
- **Smooth Animations** - Slide-in alerts, pulse effects
- **Professional Typography** - Segoe UI font family

### Color Scheme
- Primary: `#3b82f6` (Blue)
- Danger: `#ef4444` (Red)
- Success: `#10b981` (Green)
- Warning: `#f59e0b` (Orange)
- Dark: `#1f2937` (Gray)

---

## 🔐 Security Features

### 1. Thread-Safe Operations
- All data structures protected with locks
- Concurrent request handling
- No race conditions

### 2. Automatic Cleanup
- Background thread removes old timestamps
- Expired blocks automatically removed
- Memory-efficient operation

### 3. Rate Limiting
- Per-IP request tracking
- Sliding window algorithm
- Configurable thresholds

### 4. Logging
- All attacks logged to file
- Timestamp and IP recorded
- Persistent storage

---

## ⚙️ Customization

### Change Detection Parameters

Edit `app.py`:
```python
REQUEST_THRESHOLD = 30      # Allow 30 requests/min
BLOCK_DURATION = 600        # Block for 10 minutes
MONITOR_WINDOW = 120        # Monitor 2-minute window
```

### Change Server Ports

**Detection Server:**
```python
app.run(host='127.0.0.1', port=9000, debug=False)
```

**Target Server:**
```python
app.run(host='127.0.0.1', port=6000, debug=False)
```

### Customize Dashboard Refresh Rate

Edit `static/js/dashboard.js`:
```javascript
refreshInterval = setInterval(refreshData, 5000); // 5 seconds
```

---

## 📝 Log File Format

Location: `logs/attack_log.txt`

Format:
```
[2025-11-01 12:30:45] ALERT: 127.0.0.1 exceeded threshold with 25 requests - BLOCKED for 300s
[2025-11-01 12:35:20] ALERT: 192.168.1.100 exceeded threshold with 30 requests - BLOCKED for 300s
[2025-11-01 12:40:00] Logs cleared
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Issue: Module Not Found
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Dashboard Not Updating
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- Check browser console for errors
- Verify detection server is running

### Issue: Can't Connect to Target Server
- Ensure `target_server.py` is running
- Check http://127.0.0.1:5000 in browser
- Look for error messages in terminal

---

## 🎓 Educational Value

### Learning Outcomes
- Understanding DoS attacks
- Rate limiting implementation
- Real-time web applications
- Flask framework
- JavaScript async operations
- Chart.js visualization
- Thread-safe programming
- RESTful API design

### Concepts Demonstrated
- **Backend:** Flask routing, threading, data structures
- **Frontend:** AJAX, DOM manipulation, Chart.js
- **Security:** Rate limiting, IP blocking, logging
- **Architecture:** Client-server model, API design

---

## 📚 Project Highlights for Presentation

### 1. Real-World Application
- Simulates actual DoS detection systems
- Used by major websites and services
- Practical security implementation

### 2. Technical Complexity
- Multi-threaded backend
- Real-time data processing
- Thread-safe operations
- Efficient algorithms

### 3. User Experience
- Professional dashboard
- Real-time updates
- Visual feedback
- Easy to use

### 4. Completeness
- Full-stack implementation
- Testing tools included
- Comprehensive documentation
- Production-ready code

---

## 🏆 Features That Stand Out

✨ **Real-time Monitoring** - Live updates without page refresh
✨ **Visual Analytics** - Beautiful charts and graphs
✨ **Automatic Detection** - No manual intervention needed
✨ **Smart Blocking** - Temporary blocks with auto-unblock
✨ **Comprehensive Logging** - Persistent attack records
✨ **Testing Suite** - Built-in attack simulator
✨ **Professional UI** - Modern, responsive design
✨ **Well Documented** - Extensive guides and comments

---

## 📄 Files Description

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | ~200 | Main detection server with API |
| `target_server.py` | ~150 | Simulated victim website |
| `attack_simulator.py` | ~250 | Attack testing tool |
| `dashboard.html` | ~150 | Dashboard interface |
| `style.css` | ~400 | Professional styling |
| `dashboard.js` | ~200 | Real-time updates |

**Total:** ~1,350 lines of code

---

## 🎯 Use Cases

1. **Educational:** Learn about DoS attacks and prevention
2. **Testing:** Test web applications under load
3. **Development:** Prototype security features
4. **Demonstration:** Show security concepts visually
5. **Research:** Study attack patterns and detection

---

## 🔮 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Email/SMS alerts
- [ ] Whitelist/blacklist management
- [ ] Geographic IP tracking
- [ ] Machine learning detection
- [ ] Docker containerization
- [ ] Cloud deployment support
- [ ] Advanced analytics dashboard

---

## 📞 Support & Documentation

- **Setup Guide:** See `SETUP_GUIDE.md`
- **Usage Instructions:** See `USAGE_INSTRUCTIONS.md`
- **Code Comments:** Extensive inline documentation
- **API Documentation:** See API Endpoints section above

---

## 📜 License

This project is created for educational and testing purposes only.

---

## 👨‍💻 Development Info

- **Language:** Python 3.10+
- **Framework:** Flask 3.0.0
- **Frontend:** Vanilla JavaScript (No frameworks)
- **Styling:** Custom CSS (No frameworks)
- **Charts:** Chart.js 4.4.0

---

## ✅ Project Checklist

- [x] Backend detection server
- [x] Target server simulation
- [x] Attack simulator tool
- [x] Real-time dashboard
- [x] Visual charts and graphs
- [x] IP blocking mechanism
- [x] Attack logging
- [x] Auto-unblock feature
- [x] Thread-safe operations
- [x] API endpoints
- [x] Responsive design
- [x] Comprehensive documentation

---

## 🎉 Conclusion

This DoS Detection and Prevention System is a complete, production-ready application that demonstrates advanced web development, security concepts, and real-time data processing. It's perfect for educational purposes, presentations, and understanding how modern security systems work.

**Ready to test? Start the servers and open the dashboard!** 🚀

---

**Project Status:** ✅ Complete and Ready for Demonstration

**Last Updated:** November 1, 2025
