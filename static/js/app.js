// app.js - Frontend JavaScript for PlantCare AI

let selectedFile = null;
let currentImageUrl = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('PlantCare AI Initialized');
    
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', handleImageSelect);
    }
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
});

function handleImageSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) {
        alert('Image too large. Max 10MB');
        return;
    }
    
    selectedFile = file;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        currentImageUrl = e.target.result;
        showPreview(currentImageUrl);
    };
    reader.readAsDataURL(file);
}

function showPreview(imageUrl) {
    document.getElementById('uploadSection').classList.add('hidden');
    document.getElementById('previewSection').classList.remove('hidden');
    document.getElementById('previewImage').src = imageUrl;
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

async function analyzeImage() {
    if (!selectedFile) {
        alert('No image selected');
        return;
    }
    
    document.getElementById('previewSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.remove('hidden');
    
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('HTTP error! status: ' + response.status);
        }
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result.data);
        } else {
            alert('Analysis failed: ' + result.message);
            resetApp();
        }
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error analyzing image. Please try again.');
        resetApp();
    }
}

function displayResults(data) {
    document.getElementById('loadingSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');
    document.getElementById('resultImage').src = currentImageUrl;
    document.getElementById('plantName').textContent = data.plantName;
    document.getElementById('confidence').textContent = data.confidence + '%';
    // Add confidence bar
    const confidencePercent = data.confidence;
    let barColor = 'bg-green-500';
    if (confidencePercent < 60) barColor = 'bg-red-500';
    else if (confidencePercent < 70) barColor = 'bg-orange-500';
    else if (confidencePercent < 85) barColor = 'bg-yellow-500';
    
    const confidenceContainer = document.getElementById('confidence').parentElement;
    confidenceContainer.innerHTML = `
        <div class="flex-1">
            <div class="flex items-center justify-between mb-1">
                <span class="text-gray-600 text-sm">Confidence</span>
                <span class="font-bold text-gray-800">${confidencePercent}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="${barColor} h-2 rounded-full transition-all duration-500" style="width: ${confidencePercent}%"></div>
            </div>
        </div>
    `;




// Handle confidence warning
    if (data.confidenceWarning) {
        const warningCard = document.getElementById('confidenceWarning');
        const warningIcon = document.getElementById('warningIcon');
        const warningMessage = document.getElementById('warningMessage');
        
        // Show warning card
        warningCard.classList.remove('hidden');
        
        // Set warning message
        warningMessage.textContent = data.confidenceWarning;
        
        // Set colors based on confidence level
        let borderColor = 'border-orange-100';
        let iconBg = 'bg-orange-100';
        let iconColor = 'text-orange-600';
        
        if (data.confidenceLevel === 'very_low') {
            borderColor = 'border-red-100';
            iconBg = 'bg-red-100';
            iconColor = 'text-red-600';
        } else if (data.confidenceLevel === 'low') {
            borderColor = 'border-orange-100';
            iconBg = 'bg-orange-100';
            iconColor = 'text-orange-600';
        } else if (data.confidenceLevel === 'medium') {
            borderColor = 'border-yellow-100';
            iconBg = 'bg-yellow-100';
            iconColor = 'text-yellow-600';
        }
        
        // Apply colors
        warningCard.className = warningCard.className.replace(/border-\w+-\d+/, borderColor);
        warningIcon.className = iconBg + ' p-3 rounded-xl';
        const icon = warningIcon.querySelector('i');
        if (icon) {
            icon.className = iconColor;
        }
    } else {
        // Hide warning if confidence is high
        document.getElementById('confidenceWarning').classList.add('hidden');
    }

    const statusBadge = document.getElementById('statusBadge');
    const isHealthy = data.healthStatus === 'Healthy';
    
    statusBadge.className = 'inline-flex items-center gap-2 px-4 py-2 rounded-full ' + 
        (isHealthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800');
    statusBadge.innerHTML = '<i data-lucide="' + (isHealthy ? 'check-circle' : 'alert-circle') + 
        '" style="width: 18px; height: 18px;"></i><span class="font-semibold">' + 
        data.healthStatus + '</span>';
    
    if (!isHealthy && data.severity && data.severity !== 'None') {
        document.getElementById('severityBadge').classList.remove('hidden');
        document.getElementById('severity').textContent = data.severity;
    }
    
    if (data.diseaseDetected) {
        document.getElementById('diseaseCard').classList.remove('hidden');
        document.getElementById('diseaseName').textContent = data.diseaseName;
        document.getElementById('diseaseDescription').textContent = data.description;
        
        const symptomsList = document.getElementById('symptomsList');
        symptomsList.innerHTML = '';
        if (data.symptoms && data.symptoms.length > 0) {
            data.symptoms.forEach(function(symptom) {
                const li = document.createElement('li');
                li.className = 'flex items-start gap-2 text-gray-700';
                li.innerHTML = '<span class="text-red-500 mt-1">•</span><span>' + symptom + '</span>';
                symptomsList.appendChild(li);
            });
        }
        
        document.getElementById('solutionsCard').classList.remove('hidden');
        const solutionsList = document.getElementById('solutionsList');
        solutionsList.innerHTML = '';
        if (data.solutions && data.solutions.length > 0) {
            data.solutions.forEach(function(solution, index) {
                const div = document.createElement('div');
                div.className = 'flex gap-3 bg-green-50 p-4 rounded-xl';
                div.innerHTML = '<div class="bg-green-200 text-green-800 font-bold w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm">' + 
                    (index + 1) + '</div><p class="text-gray-700 pt-1">' + solution + '</p>';
                solutionsList.appendChild(div);
            });
        }
    }
    
    const preventiveCareList = document.getElementById('preventiveCareList');
    preventiveCareList.innerHTML = '';
    if (data.preventiveCare && data.preventiveCare.length > 0) {
        data.preventiveCare.forEach(function(care) {
            const div = document.createElement('div');
            div.className = 'flex gap-3 bg-blue-50 p-4 rounded-xl';
            div.innerHTML = '<span class="text-blue-500">✓</span><p class="text-gray-700">' + care + '</p>';
            preventiveCareList.appendChild(div);
        });
    }
    
    const envFactors = data.environmentalFactors || {};
    document.getElementById('environmentalFactors').innerHTML = 
        '<div class="bg-gradient-to-br from-orange-50 to-orange-100 p-6 rounded-2xl text-center">' +
        '<i data-lucide="thermometer" class="text-orange-600 mx-auto mb-3" style="width: 32px; height: 32px;"></i>' +
        '<p class="text-sm text-gray-600 mb-1">Temperature</p>' +
        '<p class="font-bold text-gray-800">' + (envFactors.idealTemp || 'N/A') + '</p></div>' +
        '<div class="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-2xl text-center">' +
        '<i data-lucide="droplets" class="text-blue-600 mx-auto mb-3" style="width: 32px; height: 32px;"></i>' +
        '<p class="text-sm text-gray-600 mb-1">Humidity</p>' +
        '<p class="font-bold text-gray-800">' + (envFactors.humidity || 'N/A') + '</p></div>' +
        '<div class="bg-gradient-to-br from-yellow-50 to-yellow-100 p-6 rounded-2xl text-center">' +
        '<i data-lucide="sun" class="text-yellow-600 mx-auto mb-3" style="width: 32px; height: 32px;"></i>' +
        '<p class="text-sm text-gray-600 mb-1">Sunlight</p>' +
        '<p class="font-bold text-gray-800">' + (envFactors.sunlight || 'N/A') + '</p></div>' +
        '<div class="bg-gradient-to-br from-cyan-50 to-cyan-100 p-6 rounded-2xl text-center">' +
        '<i data-lucide="droplets" class="text-cyan-600 mx-auto mb-3" style="width: 32px; height: 32px;"></i>' +
        '<p class="text-sm text-gray-600 mb-1">Watering</p>' +
        '<p class="font-bold text-gray-800">' + (envFactors.wateringFreq || 'N/A') + '</p></div>';
    
    window.lastAnalysis = {
        plantName: data.plantName,
        diseaseName: data.diseaseName,
        severity: data.severity,
        healthStatus: data.healthStatus
    };
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function resetApp() {
    selectedFile = null;
    currentImageUrl = null;
    const imageInput = document.getElementById('imageInput');
    if (imageInput) imageInput.value = '';
    
    document.getElementById('uploadSection').classList.remove('hidden');
    document.getElementById('previewSection').classList.add('hidden');
    document.getElementById('loadingSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('diseaseCard').classList.add('hidden');
    document.getElementById('solutionsCard').classList.add('hidden');
    document.getElementById('severityBadge').classList.add('hidden');
    document.getElementById('confidenceWarning').classList.add('hidden');

    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    if (chatWindow) {
        chatWindow.classList.toggle('hidden');
        if (!chatWindow.classList.contains('hidden')) {
            const chatInput = document.getElementById('chatInput');
            if (chatInput) chatInput.focus();
        }
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    if (!input) return;
    
    const message = input.value.trim();
    if (!message) return;
    
    input.value = '';
    addChatMessage(message, 'user');
    const typingId = addTypingIndicator();
    
    try {
        const requestData = { message: message };
        if (window.lastAnalysis) {
            requestData.context = 'User analyzed ' + window.lastAnalysis.plantName + 
                '. Disease: ' + (window.lastAnalysis.diseaseName || 'Healthy') + 
                '. Status: ' + window.lastAnalysis.healthStatus;
        }
        
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        const result = await response.json();
        removeTypingIndicator(typingId);
        
        if (result.success) {
            addChatMessage(result.data.response, 'ai');
        } else {
            addChatMessage('Sorry, error occurred. Try again.', 'ai');
        }
    } catch (error) {
        console.error('Chat error:', error);
        removeTypingIndicator(typingId);
        addChatMessage('Connection error. Check internet.', 'ai');
    }
}

function addChatMessage(text, sender) {
    const messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex gap-3 animate-slide-in';
    
    const safeText = text.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    if (sender === 'user') {
        messageDiv.classList.add('flex-row-reverse');
        messageDiv.innerHTML = '<div class="bg-blue-100 p-2 rounded-full h-8 w-8 flex-shrink-0">' +
            '<i data-lucide="user" style="width: 16px; height: 16px;" class="text-blue-600"></i></div>' +
            '<div class="bg-blue-500 text-white rounded-2xl rounded-tr-none p-3 shadow-sm max-w-xs">' +
            '<p class="text-sm">' + safeText + '</p></div>';
    } else {
        messageDiv.innerHTML = '<div class="bg-purple-100 p-2 rounded-full h-8 w-8 flex-shrink-0">' +
            '<i data-lucide="bot" style="width: 16px; height: 16px;" class="text-purple-600"></i></div>' +
            '<div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-sm max-w-xs">' +
            '<p class="text-sm text-gray-700 whitespace-pre-wrap">' + safeText + '</p></div>';
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

function addTypingIndicator() {
    const messagesDiv = document.getElementById('chatMessages');
    if (!messagesDiv) return null;
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'flex gap-3';
    typingDiv.innerHTML = '<div class="bg-purple-100 p-2 rounded-full h-8 w-8 flex-shrink-0">' +
        '<i data-lucide="bot" style="width: 16px; height: 16px;" class="text-purple-600"></i></div>' +
        '<div class="bg-white rounded-2xl rounded-tl-none p-3 shadow-sm">' +
        '<div class="flex gap-1">' +
        '<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>' +
        '<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>' +
        '<div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>' +
        '</div></div>';
    
    messagesDiv.appendChild(typingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
    
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    if (!id) return;
    const indicator = document.getElementById(id);
    if (indicator) indicator.remove();
}