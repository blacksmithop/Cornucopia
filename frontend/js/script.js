document.addEventListener('DOMContentLoaded', function () {
  const chatInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatBody = document.getElementById('chat-body');

  function sendMessage() {
      const messageText = chatInput.value.trim();
      if (messageText) {
          const messageElement = document.createElement('div');
          messageElement.className = 'message user-message';
          messageElement.textContent = messageText;
          chatBody.appendChild(messageElement);
          chatInput.value = '';
          chatBody.scrollTop = chatBody.scrollHeight;
      }
  }

  sendButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keypress', function (event) {
      if (event.key === 'Enter') {
          sendMessage();
          event.preventDefault();
      }
  });
});
