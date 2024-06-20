document.addEventListener('DOMContentLoaded', function () {
    const fileUpload = document.getElementById('file-upload');
    const statusContainer = document.getElementById('status-container');

    fileUpload.addEventListener('change', function () {
        const file = fileUpload.files[0];
        if (file) {
            const fileTypeIcon = getFileTypeIcon(file.name);
            addStatusItem(`${fileTypeIcon} Processing ${file.name}...`, 3000, () => {
                addStatusItem(`Preparing ${file.name}...`, 3000, () => {
                    addStatusItem(`Adding ${file.name} to database...`, 5000, () => {
                        addSuccessItem(`Success! File name: ${file.name}`);
                    });
                });
            });
        }
    });

    function getFileTypeIcon(fileName) {
        const fileExtension = fileName.split('.').pop().toLowerCase();
        switch (fileExtension) {
            case 'xlsx':
                return '📊'; // Excel icon
            case 'docx':
                return '📄'; // Word icon
            case 'txt':
                return '📃'; // Text file icon
            case 'md':
                return '📝'; // Markdown icon
            case 'pdf':
                return '📑'; // PDF icon
            default:
                return '📁'; // Default file icon
        }
    }

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
