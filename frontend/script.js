// Dynamic API URL: Agar local me run ho raha hai toh 127.0.0.1, warna Render live backend
const API_BASE = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000"
    : "https://ai-cybersecurity-system-1.onrender.com";

async function predictThreat() {
    const btn = document.getElementById("analyze-btn");
    btn.innerText = "Analyzing Telemetry...";
    btn.disabled = true;

    const payload = {
        source_ip: document.getElementById("source_ip").value || "127.0.0.1",
        traffic_rate: parseFloat(document.getElementById("traffic").value) || 0,
        failed_logins: parseFloat(document.getElementById("failed").value) || 0,
        session_duration: parseFloat(document.getElementById("duration").value) || 60,
        bytes_transferred: parseFloat(document.getElementById("bytes").value) || 2048,
        port_scan_count: parseInt(document.getElementById("ports").value) || 1
    };

    try {
        const response = await fetch(${API_BASE}/predict, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Inference Endpoint Failure");
        const data = await response.json();

        const resultBox = document.getElementById("result-box");
        resultBox.className = erdict-card ;
        resultBox.innerHTML = 
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="font-size:1.3rem;"></h3>
                <span class="badge" style="background:; color:#fff; border:none;">
                    
                </span>
            </div>
            <p style="margin-top:0.5rem; color:#94a3b8;">Source IP: <strong></strong></p>
            <div class="score-bar">
                <div class="score-fill " style="width: %;"></div>
            </div>
            <p style="display:flex; justify-content:space-between; font-size:0.85rem;">
                <span>Threat Risk Score: <strong>%</strong></span>
                <span>Mitigation: <strong></strong></span>
            </p>
        ;

        fetchLiveLogs();
    } catch (err) {
        document.getElementById("result-box").innerHTML = 
            <div style="color:#ef4444;">
                <p><strong>Connection Error:</strong> Could not connect to API ()</p>
            </div>
        ;
    } finally {
        btn.innerText = "Analyze Incident";
        btn.disabled = false;
    }
}

async function fetchLiveLogs() {
    try {
        const res = await fetch(${API_BASE}/logs);
        if (!res.ok) return;
        const data = await res.json();
        const tbody = document.getElementById("logs-table-body");
        tbody.innerHTML = "";

        data.telemetry_stream.slice(0, 8).forEach(log => {
            const tr = document.createElement("tr");
            tr.innerHTML = 
                <td>#</td>
                <td><code></code></td>
                <td></td>
                <td></td>
                <td>%</td>
                <td><span style="color:"></span></td>
                <td><code></code></td>
            ;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error("Failed to load audit logs", e);
    }
}

window.onload = fetchLiveLogs;
