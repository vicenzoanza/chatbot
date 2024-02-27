function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    appendMessage("user", userInput);
    document.getElementById("user-input").value = "";

    // Enviar el mensaje al servidor y obtener la respuesta del chatbot
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'user_input=' + userInput
    })
    .then(response => response.json())
    .then(data => {
        var botResponse = data.response;
        appendMessage("bot", botResponse);
    })
    .catch(error => console.error('Error:', error));
}

function appendMessage(sender, message) {
    var chatBox = document.getElementById("chat-box");
    var messageDiv = document.createElement("div");
    messageDiv.className = sender;
    messageDiv.innerHTML = message;
    chatBox.appendChild(messageDiv);
}