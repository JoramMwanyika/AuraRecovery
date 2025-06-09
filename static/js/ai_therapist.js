let currentSessionId = null;
let isTyping = false;

document.addEventListener('DOMContentLoaded', function() {
    loadAIInsights();
    setupChatInterface();
    initializeMoodTracking();
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

// Initialize mood tracking functionality
function initializeMoodTracking() {
    // Initialize mood charts
    let moodHistoryChart = null;
    let moodTrendsChart = null;
    
    // Initialize charts
    initializeCharts();
    
    // Set up mood entry form
    const moodEntryForm = document.getElementById('moodEntryForm');
    if (moodEntryForm) {
        moodEntryForm.addEventListener('submit', handleMoodEntry);
    }
    
    // Set up mood selection
    const moodOptions = document.querySelectorAll('.mood-option');
    let selectedMood = null;
    
    moodOptions.forEach(option => {
        option.addEventListener('click', () => {
            moodOptions.forEach(opt => opt.classList.remove('ring-2', 'ring-blue-500'));
            option.classList.add('ring-2', 'ring-blue-500');
            selectedMood = option.dataset.mood;
        });
        
        // Keyboard navigation
        option.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                option.click();
            }
        });
    });
}

// Initialize charts
function initializeCharts() {
    // Initialize mood history chart
    const moodCtx = document.getElementById('moodChart');
    if (moodCtx) {
        moodHistoryChart = new Chart(moodCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Mood Score',
                    data: [],
                    borderColor: 'rgb(59, 130, 246)',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const moodMapping = {
                                    1: 'Very Sad',
                                    2: 'Sad',
                                    3: 'Neutral',
                                    4: 'Happy',
                                    5: 'Very Happy'
                                };
                                return `Mood: ${moodMapping[context.raw]}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 1,
                        max: 5,
                        ticks: {
                            stepSize: 1,
                            callback: function(value) {
                                const moodMapping = {
                                    1: '😢',
                                    2: '😔',
                                    3: '😐',
                                    4: '🙂',
                                    5: '😄'
                                };
                                return moodMapping[value];
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Initialize mood trends chart
    const trendsCtx = document.getElementById('moodTrendsChart');
    if (trendsCtx) {
        moodTrendsChart = new Chart(trendsCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Very Happy', 'Happy', 'Neutral', 'Sad', 'Very Sad'],
                datasets: [{
                    label: 'Mood Distribution',
                    data: [0, 0, 0, 0, 0],
                    backgroundColor: [
                        'rgb(34, 197, 94)',  // Green
                        'rgb(59, 130, 246)', // Blue
                        'rgb(156, 163, 175)', // Gray
                        'rgb(234, 179, 8)',  // Yellow
                        'rgb(239, 68, 68)'   // Red
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    // Load initial data
    loadMoodData();
}

// Load mood data from API
async function loadMoodData() {
    try {
        const response = await fetch('/api/mood/history');
        const data = await response.json();
        
        if (data.success) {
            updateMoodCharts(data);
        } else {
            console.error('Failed to load mood data:', data.message);
        }
    } catch (error) {
        console.error('Error loading mood data:', error);
    }
}

// Update mood charts with new data
function updateMoodCharts(data) {
    if (moodHistoryChart) {
        // Update mood history chart
        const dates = data.history.map(entry => entry.date);
        const moods = data.history.map(entry => entry.mood);
        
        moodHistoryChart.data.labels = dates;
        moodHistoryChart.data.datasets[0].data = moods;
        moodHistoryChart.update();
    }
    
    if (moodTrendsChart) {
        // Update mood distribution chart
        const distribution = data.distribution;
        moodTrendsChart.data.datasets[0].data = [
            distribution.very_happy,
            distribution.happy,
            distribution.neutral,
            distribution.sad,
            distribution.very_sad
        ];
        moodTrendsChart.update();
    }
}

// Handle mood entry form submission
async function handleMoodEntry(event) {
    event.preventDefault();
    
    const form = event.target;
    const selectedMood = form.querySelector('.mood-option.ring-2')?.dataset.mood;
    const notes = form.querySelector('#notes').value;
    
    if (!selectedMood) {
        showNotification('Please select a mood', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mood: selectedMood,
                notes: notes
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show success notification
            showNotification('Mood logged successfully!', 'success');
            
            // Reset form
            form.reset();
            document.querySelectorAll('.mood-option').forEach(opt => {
                opt.classList.remove('ring-2', 'ring-blue-500');
            });
            
            // Reload mood data
            loadMoodData();
            
            // Update mood analysis section if available
            if (data.analysis) {
                updateMoodAnalysis(data.analysis);
            }
        } else {
            showNotification(data.message || 'Failed to log mood', 'error');
        }
    } catch (error) {
        console.error('Error logging mood:', error);
        showNotification('An error occurred while logging your mood', 'error');
    }
}

// Update mood analysis section
function updateMoodAnalysis(analysis) {
    const analysisSection = document.querySelector('#mood-analysis-heading').closest('section');
    if (analysisSection) {
        const insightsDiv = analysisSection.querySelector('.prose');
        if (insightsDiv) {
            insightsDiv.innerHTML = analysis.analysis;
        }
    }
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform transition-transform duration-300 translate-y-0 ${
        type === 'success' ? 'bg-green-500' : 'bg-red-500'
    } text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateY(100%)';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
} 