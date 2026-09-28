const API_BASE = "https://ai-cybersecurity-system-1.onrender.com";

// Form Submission & Analysis
async function analyzeTelemetry() {
    const btn = document.querySelector("button[onclick*='analyze'], .btn-primary, button:not([class*='secondary'])");
    if (btn) {
        btn.disabled = true;
        btn.innerText = "ANALYZING...";
    }

    const payload = {
        source_ip: document.querySelector("input[placeholder*='IP'], #sourceIp, input[type='text']")?.value || "198.51.100.42",
        traffic_rate: parseFloat(document.querySelectorAll("input[type='number']")[0]?.value || 850),
        failed_logins: parseFloat(document.querySelectorAll("input[type='number']")[1]?.value || 45),
        session_duration: parseFloat(document.querySelectorAll("input[type='number']")[2]?.value || 5),
        port_scan_count: parseInt(document.querySelectorAll("input[type='number']")[3]?.value || 80),
        bytes_transferred: parseFloat(document.querySelectorAll("input[type='number']")[4]?.value || 95000)
    };

    try {
        const res = await fetch(${API_BASE}/predict, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        // Update Verdict UI Elements
        const verdictEl = document.querySelector(".status-badge, [id*='verdict'], .threat-badge");
        if (verdictEl) verdictEl.innerText = data.result;

        const scoreEl = document.querySelector(".risk-score, h1:has(+ span), strong:has(+ span)");
        if (scoreEl) scoreEl.innerText = ${data.risk_score}%;

        // Refresh audit table immediately after new prediction
        await loadAuditStream();
    } catch (e) {
        console.error("Analysis request failed:", e);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "ANALYZE TELEMETRY";
        }
    }
}

// Live Incident Audit Stream Loader
async function loadAuditStream() {
    const table = document.querySelector("table");
    if (!table) return;

    let tbody = table.querySelector("tbody");
    if (!tbody) {
        tbody = document.createElement("tbody");
        table.appendChild(tbody);
    }

    try {
        const response = await fetch(${API_BASE}/logs);
        const json = await response.json();
        const logs = json.telemetry_stream || json.logs || [];

        tbody.innerHTML = "";
        if (logs.length === 0) {
            tbody.innerHTML = "<tr><td colspan='7' style='text-align:center; padding:16px; color:#64748b;'>No incidents recorded yet.</td></tr>";
            return;
        }

        logs.slice(0, 10).forEach(log => {
            const tr = document.createElement("tr");
            const isHigh = log.severity === "HIGH";
            tr.innerHTML = 
                <td style="padding:10px; border-bottom:1px solid #1e293b;"></td>
                <td style="padding:10px; border-bottom:1px solid #1e293b; color:#38bdf8;"></td>
                <td style="padding:10px; border-bottom:1px solid #1e293b;"></td>
                <td style="padding:10px; border-bottom:1px solid #1e293b;"></td>
                <td style="padding:10px; border-bottom:1px solid #1e293b; font-weight:bold;">%</td>
                <td style="padding:10px; border-bottom:1px solid #1e293b; color:; font-weight:bold;"></td>
                <td style="padding:10px; border-bottom:1px solid #1e293b; color:;"></td>
            ;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error("Audit log stream failed:", err);
        tbody.innerHTML = "<tr><td colspan='7' style='text-align:center; padding:16px; color:#ef4444;'>Failed to stream telemetry audit trail.</td></tr>";
    }
}

// Auto init on page load
window.addEventListener("DOMContentLoaded", () => {
    loadAuditStream();
    
    // Wire refresh button
    const refreshBtn = document.querySelector("button:has-text('Refresh'), .btn-secondary, button[onclick*='fetch']");
    if (refreshBtn) {
        refreshBtn.onclick = (e) => {
            e.preventDefault();
            loadAuditStream();
        };
    }
});
