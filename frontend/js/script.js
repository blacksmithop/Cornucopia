document.addEventListener('DOMContentLoaded', function() {
    const chatWindow = document.querySelector('.chat-window');
    const inputField = document.querySelector('.form-control');
    const sendButton = document.getElementById('sendButton');
  
    const userAvatar = '<i class="fa-solid fa-user"></i>';
    const botAvatar = '<i class="fa-solid fa-robot"></i>';
  
    function appendMessage(content, className, avatarHtml) {
      const messageContainer = document.createElement('div');
      messageContainer.className = className;
  
      const messageAvatar = document.createElement('span');
      messageAvatar.innerHTML = avatarHtml;
      messageAvatar.className = 'message-avatar';
  
      const messageText = document.createElement('span');
      messageText.className = 'message-text';
      messageText.innerText = content;
  
      if (className === 'user-message') {
        messageContainer.appendChild(messageText);
        messageContainer.appendChild(messageAvatar);
      } else {
        messageContainer.appendChild(messageAvatar);
        messageContainer.appendChild(messageText);
      }
  
      chatWindow.appendChild(messageContainer);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    function simulateBotResponse() {
      const botMessage = "This is a simulated response.";
      appendMessage('', 'bot-message', botAvatar);
      const botMessageText = chatWindow.querySelector('.bot-message:last-child .message-text');
  
      let i = 0;
      const interval = setInterval(() => {
        if (i < botMessage.length) {
          botMessageText.innerText += botMessage.charAt(i);
          i++;
        } else {
          clearInterval(interval);
        }
      }, 50);
    }
  
    function sendMessage() {
      const userMessage = inputField.value;
      if (userMessage.trim() !== '') {
        appendMessage(userMessage, 'user-message', userAvatar);
        inputField.value = '';
        setTimeout(simulateBotResponse, 500);
      }
    }
  
    inputField.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  
    sendButton.addEventListener('click', sendMessage);
  });
  