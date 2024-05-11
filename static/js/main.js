document.addEventListener('DOMContentLoaded', function() {
    const sendMessageButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const conversationContainer = document.getElementById('conversation-container');

    sendMessageButton.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            displayMessage('fan', message);
            sendMessage(message);
            messageInput.value = '';
        }
    });

    function sendMessage(message) {
        // Placeholder for sending message to the backend
        fetch('/api/conversation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.reply) {
                displayMessage('ai_influencer', data.reply);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function displayMessage(sender, message) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);
        messageDiv.textContent = message;
        conversationContainer.appendChild(messageDiv);
        conversationContainer.scrollTop = conversationContainer.scrollHeight;
    }

    function initConversation() {
        // Placeholder for initializing conversation with the AI influencer
        fetch('/api/conversation/start', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.messages) {
                data.messages.forEach(msg => {
                    displayMessage(msg.sender, msg.content);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function toggleFeature(featureId) {
        // Placeholder for toggling features on and off
        fetch(`/api/features/toggle/${featureId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.status) {
                updateFeatures();
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function updateFeatures() {
        // Placeholder for updating the list of features
        fetch('/api/features', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.features) {
                const featureList = document.getElementById('feature-list');
                featureList.innerHTML = '';
                data.features.forEach(feature => {
                    const featureCard = document.createElement('div');
                    featureCard.classList.add('feature-card');
                    featureCard.textContent = feature.name;
                    featureList.appendChild(featureCard);
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function initPayment() {
        // Placeholder for initializing payment process
        fetch('/api/payment/process', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data && data.confirmation) {
                console.log('Payment successful:', data.confirmation);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Initialize the conversation when the page is loaded
    initConversation();
});