document.addEventListener('DOMContentLoaded', function () {
    const fileUpload = document.getElementById('file-upload');
    const chatBody = document.getElementById('chat-body');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');

    fileUpload.addEventListener('change', function () {
        const file = fileUpload.files[0];
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message user-message image-message';
                messageDiv.appendChild(img);
                chatBody.appendChild(messageDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            };
            reader.readAsDataURL(file);
        }
    });

    sendButton.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        if (messageText !== '') {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            messageDiv.textContent = messageText;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
            chatInput.value = '';

            // Simulate a response
            setTimeout(() => {
                const responseDiv = document.createElement('div');
                responseDiv.className = 'message system-message';
                responseDiv.textContent = 'This is a dummy response from the system.';
                chatBody.appendChild(responseDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            }, 1000);
        }
    }
});
