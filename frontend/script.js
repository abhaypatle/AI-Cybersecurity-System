async function predictThreat() {
    try {
        const traffic = parseFloat(
            document.getElementById("traffic").value
        );

        const failed = parseFloat(
            document.getElementById("failed").value
        );

        if (isNaN(traffic) || isNaN(failed)) {
            alert("Please enter valid numbers");
            return;
        }

        const response = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    traffic_rate: traffic,
                    failed_logins: failed
                })
            }
        );

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>${data.result}</h2>
            <h3>Severity: ${data.severity}</h3>
            <p>Traffic Rate: ${data.traffic_rate}</p>
            <p>Failed Logins: ${data.failed_logins}</p>
        `;
    }
    catch (error) {
        console.error(error);
        document.getElementById("result").innerHTML =
            "<h3>API Connection Error</h3>";
    }
}