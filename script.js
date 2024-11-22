document.getElementById("send-btn").addEventListener("click", async () => {
    const userInput = document.getElementById("user-input").value;

    // Prevent empty input
    if (!userInput.trim()) {
        alert("Please enter a question.");
        return;
    }

    const chatOutput = document.getElementById("chat-output");
    chatOutput.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    try {
        const response = await fetch("https://nadya-cv-chatbot-a818ec4d6c6c1.herokuapp.com/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: userInput }),
        });

        const data = await response.json();
        chatOutput.innerHTML += `<p><strong>Bot:</strong> ${data.response.join("<br>")}</p>`;
    } catch (error) {
        chatOutput.innerHTML += `<p><strong>Error:</strong> Unable to connect to the chatbot backend.</p>`;
    }

    // Clear input box
    document.getElementById("user-input").value = "";
});
