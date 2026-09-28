const API_URL = "https://ai-cybersecurity-system-1.onrender.com";

async function sendAnalysis() {
    const btn = document.getElementById("analyzeBtn");
    btn.disabled = true;
    btn.innerText = "EVALUATING PACKETS...";

    const payload = {
        source_ip: document.getElementById("sourceIp").value,
        traffic_rate: parseFloat(document.getElementById("trafficRate").value),
        failed_logins: parseFloat(document.getElementById("failedLogins").value),
        session_duration: parseFloat(document.getElementById("sessionDuration").value),
        bytes_transferred: parseFloat(document.getElementById("bytesTransferred").value),
        port_scan_count: parseInt(document.getElementById("portScanCount").value)
    };

    try {
        const response = await fetch(${API_URL}/predict, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Backend response error");
        const data = await response.json();

        // Update UI
        const isBlocked = data.severity === "HIGH";
        const vStatus = document.getElementById("verdictStatus");
        vStatus.innerText = data.result;
        vStatus.className = isBlocked ? "status-badge badge-threat" : "status-badge badge-safe";

        document.getElementById("riskScore").innerText = ${data.risk_score}%;

        const actStatus = document.getElementById("actionStatus");
        actStatus.innerText = isBlocked ? "ACTION: BLOCKED (Firewall Rule Active)" : "ACTION: PASS (Telemetry Verified)";
        actStatus.style.color = isBlocked ? "#ff1744" : "#00e676";

        // Refresh audit table
        fetchLiveLogs();
    } catch (err) {
        console.error("Predict error:", err);
    } finally {
        btn.disabled = false;
        btn.innerText = "ANALYZE TELEMETRY";
    }
}

async function fetchLiveLogs() {
    const tbody = document.getElementById("auditLogsBody");
    if (!tbody) return;

    try {
        const res = await fetch(${API_URL}/logs);
        if (!res.ok) throw new Error("Logs unreachable");
        const data = await res.json();
        const logs = data.telemetry_stream || [];

        tbody.innerHTML = "";
        if (logs.length === 0) {
            tbody.innerHTML = "<tr><td colspan='7' class='loading-cell'>No threat incidents recorded yet.</td></tr>";
            return;
        }

        logs.slice(0, 10).forEach(log => {
            const tr = document.createElement("tr");
            const isHigh = log.severity === "HIGH";
            tr.innerHTML = 
                <td></td>
                <td style="color:#00d2ff; font-weight:600;"></td>
                <td></td>
                <td></td>
                <td style="font-weight:700;">%</td>
                <td><span style="color:; font-weight:bold;"></span></td>
                <td><span style="color:; font-weight:bold;"></span></td>
            ;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Fetch logs failed:", e);
        tbody.innerHTML = "<tr><td colspan='7' style='text-align:center; color:#ff9100; padding:15px;'>Telemetry service warming up... click Refresh in 10s.</td></tr>";
    }
}

// Initial fetch on mount
window.addEventListener("DOMContentLoaded", fetchLiveLogs);
