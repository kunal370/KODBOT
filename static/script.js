document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.getElementById('chat-history');
    const userInput = document.getElementById('user-input');
    const generateBtn = document.getElementById('generate-btn');

    generateBtn.addEventListener('click', async function() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message
        addMessage('user', message);
        userInput.value = '';

        try {
            // Get response from server
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: message,
                    language: document.getElementById('language').value
                })
            });

            const data = await response.json();
            addMessage('bot', data.code, true);
        } catch (error) {
            addMessage('bot', 'Error: ' + error.message);
        }
    });

    function addMessage(sender, content, isCode = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;

        if (isCode) {
            const codeBlock = document.createElement('pre');
            codeBlock.className = 'code-block';
            codeBlock.textContent = content;
            msgDiv.appendChild(codeBlock);
        } else {
            msgDiv.textContent = content;
        }

        chatHistory.appendChild(msgDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});