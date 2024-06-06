document.getElementById('sendMessage').addEventListener('click', sendMessage);
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('userInput');
    if (userInput.value.trim() !== '') {
        appendMessage(userInput.value, 'user');
        userInput.value = '';
        setTimeout(() => {
            streamBotMessage('This is a simulated bot response');
        }, 500);
    }
}

function appendMessage(message, sender) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', sender);
    messageElement.innerHTML = `<img src="${sender === 'user' ? 'https://i.ibb.co/Q9rNbwX/user-img.png' : 'https://i.ibb.co/GxSBbyz/bot-img.png'}" alt="${sender}"><div>${message}</div>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function streamBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', 'bot');
    messageElement.innerHTML = `<img src="https://i.ibb.co/GxSBbyz/bot-img.png" alt="bot"><div id="botTyping"></div>`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    let index = 0;
    const typingInterval = setInterval(() => {
        if (index < message.length) {
            document.getElementById('botTyping').innerHTML += message[index];
            index++;
            chatMessages.scrollTop = chatMessages.scrollHeight;
        } else {
            clearInterval(typingInterval);
            finalizeBotMessage(message);
        }
    }, 50); // Adjust speed here (milliseconds per character)
}

function finalizeBotMessage(message) {
    const botTyping = document.getElementById('botTyping');
    const messageContent = botTyping.innerHTML;
    botTyping.parentElement.innerHTML = `<img src="https://i.ibb.co/GxSBbyz/bot-img.png" alt="bot"><div>${messageContent}</div>`;
}

document.getElementById('toggleTheme').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    updateThemeIcon();
});

function updateThemeIcon() {
    const themeIcon = document.getElementById('themeIcon');
    if (document.body.classList.contains('dark-mode')) {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    } else {
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    }
}

// Initial call to set the correct icon based on the current theme
updateThemeIcon();
