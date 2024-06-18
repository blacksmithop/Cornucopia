document.addEventListener('DOMContentLoaded', function () {
  const chatInput = document.getElementById('chat-input');
  const sendButton = document.getElementById('send-button');
  const chatBody = document.getElementById('chat-body');
  const fileUpload = document.getElementById('file-upload');

  function sendMessage() {
      const messageText = chatInput.value.trim();
      if (messageText) {
          const userMessageElement = document.createElement('div');
          userMessageElement.className = 'message user-message';
          userMessageElement.textContent = messageText;
          chatBody.appendChild(userMessageElement);
          chatInput.value = '';
          chatBody.scrollTop = chatBody.scrollHeight;

          // Simulate a response from the system
          setTimeout(() => {
              simulateResponse("This is a dummy response from the system.");
          }, 1000);
      }
  }

  function simulateResponse(text) {
      const systemMessageElement = document.createElement('div');
      systemMessageElement.className = 'message system-message';
      chatBody.appendChild(systemMessageElement);

      let index = 0;
      function typeCharacter() {
          if (index < text.length) {
              systemMessageElement.textContent += text.charAt(index);
              index++;
              setTimeout(typeCharacter, 50); // Adjust typing speed here
          } else {
              chatBody.scrollTop = chatBody.scrollHeight;
          }
      }
      typeCharacter();
  }

  sendButton.addEventListener('click', sendMessage);

  chatInput.addEventListener('keypress', function (event) {
      if (event.key === 'Enter') {
          sendMessage();
          event.preventDefault();
      }
  });

  fileUpload.addEventListener('change', function () {
      const file = fileUpload.files[0];
      if (file) {
          const fileMessageElement = document.createElement('div');
          fileMessageElement.className = 'message user-message';
          fileMessageElement.textContent = `File uploaded: ${file.name}`;
          chatBody.appendChild(fileMessageElement);
          chatBody.scrollTop = chatBody.scrollHeight;
      }
  });
});
