const API_URL = "http://127.0.0.1:5000/chatbot";

const sendButton = document.getElementById("send-button");
const resetButton = document.getElementById("reset-button");
const userInput = document.getElementById("user-input");
const messagesContainer = document.getElementById("messages");

const scrollToBottom = () => {
  const chatDisplay = document.getElementById("chat-display");
  chatDisplay.scrollTop = chatDisplay.scrollHeight;
};

const addMessage = (message, sender) => {
  const messageBubble = document.createElement("div");
  messageBubble.className = sender === "bot" ? "bot-message" : "user-message";
  messageBubble.textContent = message;
  messagesContainer.appendChild(messageBubble);
  scrollToBottom();
};

const resetChat = () => {
  messagesContainer.innerHTML = `
    <div class="bot-message">
      Hi! I’m Nadya’s CV Chatbot. Let’s chat about her qualifications!
    </div>
  `;
  userInput.value = "";
};

const sendMessage = async () => {
  const query = userInput.value.trim();
  if (!query) return;

  addMessage(query, "user");
  userInput.value = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (response.ok && data.response) {
      data.response.forEach((msg) => addMessage(msg, "bot"));
    } else {
      addMessage("Error communicating with the server.", "bot");
    }
  } catch (error) {
    addMessage("Error communicating with the server.", "bot");
  }
};

sendButton.addEventListener("click", sendMessage);
resetButton.addEventListener("click", resetChat);
userInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") sendMessage();
});
