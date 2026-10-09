const chatbox = document.getElementById("chatbox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

function appendMessage(sender, text) {
    const message = document.createElement("div");
    message.classList.add("message");
    message.classList.add(sender);
    message.innerText = text;
    chatbox.appendChild(message);
    chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage("user", text);
    userInput.value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage("bot", data.reply);
        const speech = new SpeechSynthesisUtterance(data.reply);
        window.speechSynthesis.speak(speech);
    })
    .catch(error => {
        console.error(error);
        appendMessage("bot", "Server error");
    });
}

sendBtn.addEventListener("click", sendMessage);
userInput.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});