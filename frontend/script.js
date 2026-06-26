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
            "https://ai-cybersecurity-system.onrender.com/predict",
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

        if (!response.ok) {
            throw new Error("API Error");
        }

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>${data.result}</h2>
            <h3>Severity: ${data.severity}</h3>
            <p><strong>Traffic Rate:</strong> ${data.traffic_rate}</p>
            <p><strong>Failed Logins:</strong> ${data.failed_logins}</p>
        `;

    } catch (error) {

        console.error(error);

        document.getElementById("result").innerHTML = `
            <h3 style="color:red;">
                API Connection Error
            </h3>
        `;
    }
}