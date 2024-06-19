document.addEventListener('DOMContentLoaded', function () {
    const fileUpload = document.getElementById('file-upload');
    const statusContainer = document.getElementById('status-container');

    fileUpload.addEventListener('change', function () {
        const file = fileUpload.files[0];
        if (file) {
            addStatusItem(`Processing ${file.name}...`, 3000, () => {
                addStatusItem(`Preparing ${file.name}...`, 3000, () => {
                    addStatusItem(`Adding ${file.name} to database...`, 5000, () => {
                        addSuccessItem(`Success! File name: ${file.name}`);
                    });
                });
            });
        }
    });

    function addStatusItem(text, delay, callback) {
        const statusItem = document.createElement('div');
        statusItem.className = 'status-item';
        statusItem.innerHTML = `<div class="spinner"></div><p>${text}</p>`;
        statusContainer.appendChild(statusItem);

        setTimeout(() => {
            statusItem.innerHTML = `<p>${text} completed.</p><span class="success-icon">✅</span>`;
            if (callback) callback();
        }, delay);
    }

    function addSuccessItem(text) {
        const statusItem = document.createElement('div');
        statusItem.className = 'status-item';
        statusItem.innerHTML = `<p>${text}</p><span class="success-icon">✅</span>`;
        statusContainer.appendChild(statusItem);
    }
});
