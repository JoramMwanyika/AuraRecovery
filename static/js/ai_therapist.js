let currentSessionId = null;
let isTyping = false;

document.addEventListener('DOMContentLoaded', function() {
    loadAIInsights();
    setupChatInterface();
});

async function loadAIInsights() {
    try {
        const response = await fetch('/api/ai/insights');
        const data = await response.json();
        
        if (response.ok) {
            updateRiskAssessment(data.risk);
            updateMoodAnalysis(data.mood);
            updateRecommendations(data.recommendations);
        } else {
            console.error('Failed to load AI insights:', data.error);
        }
    } catch (error) {
        console.error('Error loading AI insights:', error);
    }
}

function updateRiskAssessment(risk) {
    const container = document.getElementById('riskAssessment');
    container.innerHTML = `
        <div class="text-center">
            <div class="text-2xl font-bold text-${getRiskColor(risk.risk_level)} mb-2">
                ${risk.risk_level}
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">
                ${risk.analysis}
            </p>
        </div>
    `;
}

function updateMoodAnalysis(mood) {
    const container = document.getElementById('moodAnalysis');
    container.innerHTML = `
        <div class="text-center">
            <div class="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                ${mood.analysis.trend}
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">
                ${mood.analysis.analysis}
            </p>
        </div>
    `;
}

function updateRecommendations(recommendations) {
    const container = document.getElementById('aiRecommendations');
    container.innerHTML = recommendations.slice(0, 3).map(rec => `
        <div class="flex items-start space-x-3">
            <div class="w-6 h-6 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center flex-shrink-0">
                <i data-lucide="check" class="w-4 h-4 text-green-600 dark:text-green-400"></i>
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">${rec.message}</p>
        </div>
    `).join('');
}

function getRiskColor(riskLevel) {
    const colors = {
        'low': 'green-600 dark:text-green-400',
        'moderate': 'yellow-600 dark:text-yellow-400',
        'high': 'red-600 dark:text-red-400'
    };
    return colors[riskLevel.toLowerCase()] || 'gray-600 dark:text-gray-400';
}

function setupChatInterface() {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const charCount = document.getElementById('charCount');
    const chatForm = document.getElementById('chatForm');
    const chatMessages = document.getElementById('chatMessages');

    // Character counter
    messageInput.addEventListener('input', function() {
        const length = this.value.length;
        charCount.textContent = `${length}/500`;
        sendButton.disabled = length === 0 || isTyping;
    });

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message && !isTyping) {
            await sendMessage(message);
        }
    });

    // Handle Enter key (Shift+Enter for new line)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (messageInput.value.trim() && !isTyping) {
                sendMessage(messageInput.value.trim());
            }
        }
    });
}

async function sendMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    
    // Add user message
    appendMessage('user', message);
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    document.getElementById('charCount').textContent = '0/500';
    
    // Show typing indicator
    isTyping = true;
    sendButton.disabled = true;
    appendTypingIndicator();
    
    try {
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (response.ok) {
            appendMessage('ai', data.message);
            
            // If urgent response, show crisis resources
            if (data.urgent) {
                document.getElementById('crisisResources').classList.remove('hidden');
            }
            
            // Refresh insights after chat
            loadAIInsights();
        } else {
            appendMessage('ai', 'I apologize, but I encountered an error. Please try again later.');
            console.error('Chat error:', data.error);
        }
    } catch (error) {
        removeTypingIndicator();
        appendMessage('ai', 'I apologize, but I encountered an error. Please try again later.');
        console.error('Chat error:', error);
    }
    
    isTyping = false;
    sendButton.disabled = false;
}

function appendMessage(sender, message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex items-start space-x-3';
    
    const icon = sender === 'user' ? 'user' : 'bot';
    const bgColor = sender === 'user' ? 'bg-purple-500' : 'bg-purple-500';
    
    messageDiv.innerHTML = `
        <div class="w-8 h-8 ${bgColor} rounded-full flex items-center justify-center flex-shrink-0">
            <i data-lucide="${icon}" class="w-4 h-4 text-white"></i>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg px-4 py-3 max-w-xs lg:max-w-md shadow-sm">
            <p class="text-gray-800 dark:text-gray-200">${message}</p>
            <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">${sender === 'user' ? 'You' : 'AI Therapist'} • Just now</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const indicator = document.createElement('div');
    indicator.id = 'typingIndicator';
    indicator.className = 'flex items-start space-x-3';
    indicator.innerHTML = `
        <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
            <i data-lucide="bot" class="w-4 h-4 text-white"></i>
        </div>
        <div class="bg-white dark:bg-gray-800 rounded-lg px-4 py-3 shadow-sm">
            <div class="flex space-x-2">
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
            </div>
        </div>
    `;
    chatMessages.appendChild(indicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

function sendQuickMessage(message) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = message;
    messageInput.dispatchEvent(new Event('input'));
    sendMessage(message);
} 