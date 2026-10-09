from flask import Flask, request, jsonify, render_template_string
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Apni Groq API key yahan daalo (console.groq.com se lo)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Chat history store karne ke liye
chat_sessions = {}

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Chatbot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; height: 100vh; display: flex; justify-content: center; align-items: center; }
        .chat-container { width: 700px; height: 800px; background: white; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #075e54; color: white; padding: 15px 20px; font-size: 18px; font-weight: bold; }
        .chat-messages { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .message { max-width: 80%; padding: 10px 14px; border-radius: 12px; font-size: 14px; line-height: 1.5; }
        .user-message { background: #dcf8c6; align-self: flex-end; border-bottom-right-radius: 3px; }
        .bot-message { background: #f1f1f1; align-self: flex-start; border-bottom-left-radius: 3px; }
        .chat-input { display: flex; padding: 10px; border-top: 1px solid #ddd; gap: 8px; }
        .chat-input input { flex: 1; padding: 10px 14px; border: 1px solid #ddd; border-radius: 25px; outline: none; font-size: 14px; }
        .chat-input button { background: #075e54; color: white; border: none; padding: 10px 18px; border-radius: 25px; cursor: pointer; font-size: 14px; }
        .chat-input button:hover { background: #128c7e; }
        .typing { color: #999; font-style: italic; font-size: 13px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">🤖 AI Chatbot</div>
        <div class="chat-messages" id="messages">
            <div class="message bot-message">Salaam! Main aapki kaise madad kar sakta hoon? 😊</div>
        </div>
        <div class="chat-input">
            <input type="text" id="userInput" placeholder="Message likhein..." onkeypress="handleKey(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const messages = document.getElementById('messages');
            const userText = input.value.trim();
            if (!userText) return;

            messages.innerHTML += `<div class="message user-message">${userText}</div>`;
            input.value = '';

            const typingDiv = document.createElement('div');
            typingDiv.className = 'message bot-message typing';
            typingDiv.id = 'typing';
            typingDiv.textContent = 'Likh raha hoon...';
            messages.appendChild(typingDiv);
            messages.scrollTop = messages.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: userText })
                });
                const data = await response.json();
                document.getElementById('typing').remove();
                messages.innerHTML += `<div class="message bot-message">${data.reply}</div>`;
            } catch (error) {
                document.getElementById('typing').remove();
                messages.innerHTML += `<div class="message bot-message">Error aa gaya, dobara try karo.</div>`;
            }
            messages.scrollTop = messages.scrollHeight;
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    session_id = request.remote_addr

    if not user_message:
        return jsonify({"reply": "Kuch likho please!"})

    # Chat history initialize karo
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    # User message history mein add karo
    chat_sessions[session_id].append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # Free aur fast model
            messages=chat_sessions[session_id],
            max_tokens=1024
        )
        reply = response.choices[0].message.content

        # Assistant reply bhi history mein save karo
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)