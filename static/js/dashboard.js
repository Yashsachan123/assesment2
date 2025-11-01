// DoS Detection System - Dashboard JavaScript

let trafficChart = null;
let refreshInterval = null;

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    startAutoRefresh();
    updateLastUpdateTime();
});

// Initialize traffic chart
function initializeChart() {
    const ctx = document.getElementById('trafficChart').getContext('2d');
    
    trafficChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Total Requests',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Blocked IPs',
                    data: [],
                    borderColor: '#ef4444',
                    backgroundColor: 'rgba(239, 68, 68, 0.1)',
                    borderWidth: 2,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}

// Start auto-refresh
function startAutoRefresh() {
    refreshData();
    refreshInterval = setInterval(refreshData, 3000); // Refresh every 3 seconds
}

// Fetch and update dashboard data
async function refreshData() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update header stats
        document.getElementById('totalRequests').textContent = data.total_requests;
        document.getElementById('blockedCount').textContent = data.total_blocked;
        
        // Update IP table
        updateIPTable(data.ip_stats);
        
        // Update blocked IPs list
        updateBlockedIPs(data.blocked_ips);
        
        // Update attack log
        updateAttackLog(data.attack_log);
        
        // Update traffic chart
        updateChart(data.traffic_history);
        
        // Show alert if there are blocked IPs
        if (data.total_blocked > 0) {
            showAlert(`${data.total_blocked} IP(s) currently blocked due to suspicious activity`);
        } else {
            hideAlert();
        }
        
        // Update last update time
        updateLastUpdateTime();
        
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

// Update IP activity table
function updateIPTable(ipStats) {
    const tbody = document.getElementById('ipTableBody');
    
    if (ipStats.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" class="no-data">No active connections</td></tr>';
        return;
    }
    
    tbody.innerHTML = ipStats.map(ip => `
        <tr>
            <td><strong>${ip.ip}</strong></td>
            <td>${ip.count}</td>
            <td>
                <span class="status-badge ${ip.status === 'BLOCKED' ? 'blocked' : 'active'}">
                    ${ip.status}
                </span>
            </td>
            <td>${ip.last_seen}</td>
        </tr>
    `).join('');
}

// Update blocked IPs list
function updateBlockedIPs(blockedIPs) {
    const container = document.getElementById('blockedIpsList');
    
    if (blockedIPs.length === 0) {
        container.innerHTML = '<p class="no-data">No blocked IPs</p>';
        return;
    }
    
    container.innerHTML = blockedIPs.map(item => `
        <div class="blocked-item">
            <span class="blocked-ip">🚫 ${item.ip}</span>
            <span class="unblock-time">Unblock: ${item.unblock_time}</span>
        </div>
    `).join('');
}

// Update attack log
function updateAttackLog(attackLog) {
    const container = document.getElementById('attackLog');
    
    if (attackLog.length === 0) {
        container.innerHTML = '<p class="no-data">No attacks detected</p>';
        return;
    }
    
    container.innerHTML = attackLog.map(entry => `
        <div class="log-entry">
            <div class="log-timestamp">[${entry.timestamp}]</div>
            <div>
                ⚠️ ALERT: <span class="log-ip">${entry.ip}</span> 
                exceeded threshold with <strong>${entry.count}</strong> requests - 
                <strong>${entry.status}</strong>
            </div>
        </div>
    `).join('');
    
    // Scroll to bottom to show latest entries
    container.scrollTop = container.scrollHeight;
}

// Update traffic chart
function updateChart(trafficHistory) {
    if (!trafficChart || trafficHistory.length === 0) return;
    
    const labels = trafficHistory.map(item => item.time);
    const requestsData = trafficHistory.map(item => item.requests);
    const blockedData = trafficHistory.map(item => item.blocked_ips);
    
    trafficChart.data.labels = labels;
    trafficChart.data.datasets[0].data = requestsData;
    trafficChart.data.datasets[1].data = blockedData;
    trafficChart.update('none'); // Update without animation for smoother real-time updates
}

// Show alert banner
function showAlert(message) {
    const banner = document.getElementById('alertBanner');
    const messageElement = document.getElementById('alertMessage');
    
    messageElement.textContent = message;
    banner.classList.remove('hidden');
}

// Hide alert banner
function hideAlert() {
    const banner = document.getElementById('alertBanner');
    banner.classList.add('hidden');
}

// Update last update time
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = timeString;
}

// Simulate a test request
async function simulateRequest() {
    try {
        const response = await fetch('/api/simulate_request');
        const data = await response.json();
        
        if (data.allowed) {
            alert(`✅ Request allowed from ${data.ip}\n${data.message}`);
        } else {
            alert(`🚫 Request blocked from ${data.ip}\n${data.message}`);
        }
        
        // Refresh data immediately
        refreshData();
        
    } catch (error) {
        console.error('Error simulating request:', error);
        alert('❌ Error simulating request');
    }
}

// Clear all logs
async function clearLogs() {
    if (!confirm('Are you sure you want to clear all logs and reset tracking?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/clear_logs');
        const data = await response.json();
        
        if (data.status === 'success') {
            alert('✅ ' + data.message);
            refreshData();
        }
        
    } catch (error) {
        console.error('Error clearing logs:', error);
        alert('❌ Error clearing logs');
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
