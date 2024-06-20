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
    const modal = document.getElementById('steps-modal');
    const closeModal = document.querySelector('.close');
    const stepsContent = document.getElementById('steps-content');

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

    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
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

                // Add view steps button
                const viewStepsButton = document.createElement('button');
                viewStepsButton.className = 'view-steps-button';
                viewStepsButton.innerHTML = '👁️';
                responseDiv.appendChild(viewStepsButton);

                viewStepsButton.addEventListener('click', function () {
                    showSteps(data.steps);
                });

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

    function showSteps(steps) {
        stepsContent.innerHTML = '';
        steps.forEach((step, index) => {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'step';
            const stepInfo = step[0];
            const stepResult = step[1];
            stepDiv.innerHTML = `<strong>Step ${index + 1}:</strong><br> 
                                 <strong>Tool:</strong> ${stepInfo.tool}<br>
                                 <strong>Tool Input:</strong> ${stepInfo.tool_input}<br>
                                 <strong>Log:</strong> ${stepInfo.log}<br>
                                 <strong>Type:</strong> ${stepInfo.type}<br>
                                 <strong>Result:</strong> <span class="result-content">${stepResult.substring(0, 100)}...</span><button class="show-more-button">View Less</button><div class="step-content"><p>${stepResult}</p></div>`;
            stepsContent.appendChild(stepDiv);

            const showMoreButton = stepDiv.querySelector('.show-more-button');
            const stepContent = stepDiv.querySelector('.step-content');

            showMoreButton.addEventListener('click', function () {
                const isHidden = stepContent.style.display === 'none' || stepContent.style.display === '';
                stepContent.style.display = isHidden ? 'block' : 'none';
                showMoreButton.textContent = isHidden ? 'View More' : 'View Less';
            });

            // Initialize with 'View Less'
            stepContent.style.display = 'none';
            showMoreButton.textContent = 'View More';
        });
        modal.style.display = 'block';
    }
});
