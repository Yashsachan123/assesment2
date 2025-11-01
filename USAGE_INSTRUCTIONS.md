# DoS Detection System - Quick Usage Instructions

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Servers (Open 2 Terminals)

**Terminal 1 - Target Server:**
```bash
python target_server.py
```
✅ Server running at: http://127.0.0.1:5000

**Terminal 2 - Detection Server:**
```bash
python app.py
```
✅ Dashboard at: http://127.0.0.1:8000

### Step 3: Open Dashboard
Open browser → http://127.0.0.1:8000

---

## 🧪 Testing Options

### Option A: Use Dashboard Test Button
1. Open http://127.0.0.1:8000
2. Click "Send Test Request" button 25+ times rapidly
3. Watch your IP get blocked!

### Option B: Use Attack Simulator
```bash
python attack_simulator.py
```
Then select:
- **Option 1:** Normal traffic (won't trigger)
- **Option 2:** DoS attack (will trigger blocking)
- **Option 3:** Distributed attack (multiple threads)

### Option C: Manual Browser Testing
1. Open http://127.0.0.1:5000 in browser
2. Refresh page rapidly 25+ times
3. Check dashboard to see blocking

---

## 📊 What to Look For

### ✅ Normal Behavior:
- Requests appear in "Active IP Addresses" table
- Request count increases slowly
- Status shows "ACTIVE"
- No alerts

### 🚨 Attack Detected:
- Red alert banner appears at top
- IP status changes to "BLOCKED"
- Entry appears in "Recent Attack Log"
- IP listed in "Blocked IP Addresses"
- Request count stops increasing

---

## 🎯 Detection Rules

| Condition | Action |
|-----------|--------|
| ≤ 20 requests/minute | ✅ Allowed |
| > 20 requests/minute | 🚫 Blocked for 5 minutes |
| After 5 minutes | ✅ Auto-unblocked |

---

## 📝 Common Commands

### Check if Python is installed:
```bash
python --version
```

### Install dependencies:
```bash
pip install flask requests
```

### Stop a running server:
Press `Ctrl + C` in the terminal

### Clear logs:
Click "Clear Logs" button in dashboard

### View log file:
```bash
cat logs/attack_log.txt
```

---

## 🔍 Verification Checklist

Before testing, verify:
- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Target server running (port 5000)
- [ ] Detection server running (port 8000)
- [ ] Dashboard accessible in browser
- [ ] No firewall blocking localhost

---

## 💡 Tips for Demonstration

1. **Start Clean:**
   - Click "Clear Logs" before demo
   - Restart both servers

2. **Show Normal Traffic First:**
   - Send 5-10 requests slowly
   - Show they're all allowed

3. **Trigger Attack:**
   - Use simulator or rapid clicking
   - Point out when blocking occurs

4. **Highlight Features:**
   - Real-time chart updates
   - Automatic blocking
   - Log entries
   - Auto-unblock timer

5. **Explain the Code:**
   - Show `app.py` detection logic
   - Explain threshold checking
   - Demonstrate thread-safe operations

---

## 🎓 For Viva/Presentation

### Questions You Might Be Asked:

**Q: How does the system detect attacks?**
A: Tracks requests per IP in 60-second window. If > 20 requests, IP is blocked.

**Q: What happens to blocked IPs?**
A: Blocked for 5 minutes, then automatically unblocked.

**Q: How is data stored?**
A: In-memory dictionaries for real-time tracking, text file for persistent logs.

**Q: Can you change the threshold?**
A: Yes, edit `REQUEST_THRESHOLD` in `app.py`.

**Q: How does the dashboard update?**
A: JavaScript fetches `/api/stats` every 3 seconds via AJAX.

**Q: What if the server crashes?**
A: In-memory data is lost, but logs persist in `attack_log.txt`.

---

## 🐛 Quick Fixes

### Dashboard not loading?
```bash
# Check if server is running
curl http://127.0.0.1:8000
```

### Can't install dependencies?
```bash
# Upgrade pip first
pip install --upgrade pip
pip install -r requirements.txt
```

### Port already in use?
```bash
# Change port in app.py or target_server.py
# Or kill existing process
lsof -i :8000
kill -9 <PID>
```

---

## 📞 Need Help?

1. Read `SETUP_GUIDE.md` for detailed instructions
2. Check code comments in Python files
3. Review error messages in terminal
4. Test with attack simulator first

---

**Good Luck! 🎉**
