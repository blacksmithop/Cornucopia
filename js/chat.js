document.addEventListener('DOMContentLoaded', function () {
    // Generate and store UUID if not already present in session storage
    if (!sessionStorage.getItem('uuid')) {
        const uuid = generateUUID();
        sessionStorage.setItem('uuid', uuid);
        console.log('Generated UUID:', uuid);
    } else {
        console.log('Existing UUID:', sessionStorage.getItem('uuid'));
    }

    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // Chat functionality
    const fileUpload = document.getElementById('file-upload');
    const chatBody = document.getElementById('chat-body');
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-button');
    const clearChatButton = document.getElementById('clear-chat');

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

    clearChatButton.addEventListener('click', function (e) {
        chatBody.innerHTML = '';
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message system-message';
        welcomeMessage.textContent = 'Hello! How can I help you today?';
        chatBody.appendChild(welcomeMessage);
    });

    function sendMessage() {
        const messageText = chatInput.value.trim();
        const sessionId = sessionStorage.getItem('uuid');
        
        if (messageText !== '') {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user-message';
            messageDiv.textContent = messageText;
            chatBody.appendChild(messageDiv);
            chatBody.scrollTop = chatBody.scrollHeight;
            chatInput.value = '';

            // Create spinner
            const spinnerDiv = document.createElement('div');
            spinnerDiv.className = 'message system-message spinner';
            spinnerDiv.innerHTML = '<div class="loader"></div>';
            chatBody.appendChild(spinnerDiv);
            chatBody.scrollTop = chatBody.scrollHeight;

            // Create an AbortController to manage the timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 60000); // 1 minute timeout

            // Send POST request to the server
            fetch('http://localhost/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText, session_id: sessionId }),
                signal: controller.signal,
            })
            .then(response => response.json())
            .then(data => {
                clearTimeout(timeoutId); // Clear the timeout
                chatBody.removeChild(spinnerDiv); // Remove the spinner
                const responseDiv = document.createElement('div');
                responseDiv.className = 'message system-message';
                responseDiv.textContent = data.response; // Assuming the response structure contains a 'response' field
                chatBody.appendChild(responseDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                clearTimeout(timeoutId); // Clear the timeout
                chatBody.removeChild(spinnerDiv); // Remove the spinner
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message system-message error-message';
                if (error.name === 'AbortError') {
                    console.error('Fetch request timed out');
                    errorDiv.textContent = 'Request timed out. Please try again.';
                } else {
                    console.error('Error:', error);
                    errorDiv.textContent = 'An error occurred. Please try again.';
                }
                chatBody.appendChild(errorDiv);
                chatBody.scrollTop = chatBody.scrollHeight;
            });
        }
    }
});
