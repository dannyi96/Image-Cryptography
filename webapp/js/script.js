// Global state
let currentMode = 'encrypt';
let inputImageLoaded = false;
let keyLoaded = false;

// DOM elements
const elements = {
    inputImg: document.getElementById('input-img'),
    outputImg: document.getElementById('output-img'),
    transformBtn: document.getElementById('transform-img-btn'),
    loadingOverlay: document.getElementById('loading-overlay'),
    loadingText: document.getElementById('loading-text'),
    progressFill: document.getElementById('progress-fill'),
    statusMessages: document.getElementById('status-messages'),
    infoModal: document.getElementById('info-modal'),
    parametersSection: document.getElementById('parameters-section'),
    uploadSection: document.getElementById('upload-section'),
    decryptUploadSection: document.getElementById('decrypt-upload-section'),
    downloadSection: document.getElementById('download-section'),
    inputInfo: document.getElementById('input-info'),
    outputInfo: document.getElementById('output-info'),
    performanceInfo: document.getElementById('performance-info'),
    processTime: document.getElementById('process-time'),
    alphaInput: document.getElementById('alpha-input'),
    iterInput: document.getElementById('iter-input'),
    actionIcon: document.getElementById('action-icon'),
    actionText: document.getElementById('action-text')
};

// Utility functions
function showStatus(message, type = 'info', duration = 3000) {
    const statusDiv = document.createElement('div');
    statusDiv.className = `status-message ${type}`;
    statusDiv.textContent = message;
    
    elements.statusMessages.appendChild(statusDiv);
    
    setTimeout(() => {
        statusDiv.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => statusDiv.remove(), 300);
    }, duration);
}

function updateProgress(percent) {
    elements.progressFill.style.width = `${percent}%`;
}

function showLoading(text = 'Processing image...') {
    elements.loadingText.textContent = text;
    elements.loadingOverlay.style.display = 'flex';
    updateProgress(0);
}

function hideLoading() {
    elements.loadingOverlay.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getImageInfo(file) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = function() {
            resolve({
                width: this.width,
                height: this.height,
                size: formatFileSize(file.size),
                type: file.type
            });
        };
        img.src = URL.createObjectURL(file);
    });
}

function updateImageInfo(info, elementId) {
    const element = document.getElementById(elementId);
    if (info) {
        element.textContent = `${info.width}×${info.height} • ${info.size}`;
    } else {
        element.textContent = '';
    }
}

function validateInputs() {
    const alpha = parseInt(elements.alphaInput.value);
    const iter = parseInt(elements.iterInput.value);
    
    if (alpha < 1 || alpha > 16) {
        showStatus('Alpha must be between 1 and 16', 'error');
        return false;
    }
    
    if (iter < 1 || iter > 50) {
        showStatus('Iterations must be between 1 and 50', 'error');
        return false;
    }
    
    return true;
}

function updateActionButton() {
    const canProcess = currentMode === 'encrypt' ? inputImageLoaded : (inputImageLoaded && keyLoaded);
    elements.transformBtn.disabled = !canProcess;
    
    if (canProcess) {
        elements.transformBtn.style.opacity = '1';
    } else {
        elements.transformBtn.style.opacity = '0.6';
    }
}

// Image preview function
function previewImage(event, imageId) {
    const input = event.target;
    const image = document.getElementById(imageId);
    const file = input.files[0];

    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showStatus('Please select a valid image file', 'error');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            showStatus('Image size must be less than 10MB', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = async function(e) {
            image.src = e.target.result;
            inputImageLoaded = true;
            
            // Get and display image info
            const info = await getImageInfo(file);
            updateImageInfo(info, 'input-info');
            
            updateActionButton();
            showStatus('Image loaded successfully', 'success');
        };
        reader.readAsDataURL(file);
    }
}

// Key file preview function
function previewText(event, divContainerId) {
    const input = event.target;
    const container = document.getElementById(divContainerId);
    const file = input.files[0];

    if (file) {
        if (file.size > 1024 * 1024) { // 1MB limit for key files
            showStatus('Key file too large', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                // Validate key format
                const keyContent = e.target.result;
                container.textContent = keyContent;
                keyLoaded = true;
                updateActionButton();
                showStatus('Key file loaded successfully', 'success');
            } catch (error) {
                showStatus('Invalid key file format', 'error');
            }
        };
        reader.readAsText(file);
    }
}

// Download functions
function downloadImage(imgId, fileName) {
    const img = document.getElementById(imgId);
    if (img.src.includes('placeholder')) {
        showStatus('No image to download', 'error');
        return;
    }

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    ctx.drawImage(img, 0, 0);
    
    canvas.toBlob(function(blob) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showStatus('Image downloaded successfully', 'success');
    }, 'image/png');
}

function downloadKey(divId, fileName) {
    const keyContent = document.getElementById(divId).textContent;
    if (!keyContent) {
        showStatus('No key to download', 'error');
        return;
    }

    const blob = new Blob([keyContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showStatus('Key downloaded successfully', 'success');
}

// Mode switching
function switchMode(mode) {
    currentMode = mode;
    
    // Update navigation
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
    
    // Update UI based on mode
    if (mode === 'encrypt') {
        elements.parametersSection.style.display = 'block';
        elements.uploadSection.style.display = 'flex';
        elements.decryptUploadSection.style.display = 'none';
        elements.downloadSection.style.display = 'flex';
        elements.actionText.textContent = 'Encrypt';
        elements.actionIcon.className = 'fas fa-lock';
        keyLoaded = true; // Don't need key for encryption
    } else {
        elements.parametersSection.style.display = 'none';
        elements.uploadSection.style.display = 'none';
        elements.decryptUploadSection.style.display = 'flex';
        elements.downloadSection.style.display = 'none';
        elements.actionText.textContent = 'Decrypt';
        elements.actionIcon.className = 'fas fa-unlock';
        keyLoaded = false; // Need key for decryption
    }
    
    // Reset state
    inputImageLoaded = false;
    elements.inputImg.src = './assets/imgs/placeholder.png';
    elements.outputImg.src = './assets/imgs/placeholder.png';
    updateImageInfo(null, 'input-info');
    updateImageInfo(null, 'output-info');
    elements.performanceInfo.style.display = 'none';
    
    updateActionButton();
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    document.getElementById('encrypt-nav-item').addEventListener('click', () => switchMode('encrypt'));
    document.getElementById('decrypt-nav-item').addEventListener('click', () => switchMode('decrypt'));
    
    // File uploads
    document.getElementById('img-uploader-btn').addEventListener('click', function() {
        document.getElementById('img-input').click();
    });
    
    document.getElementById('encrypted-img-uploader-btn').addEventListener('click', function() {
        document.getElementById('encrypted-img-input').click();
    });
    
    document.getElementById('key-uploader-btn').addEventListener('click', function() {
        document.getElementById('key-input').click();
    });
    
    // File inputs
    document.getElementById('img-input').addEventListener('change', function(e) {
        previewImage(e, 'input-img');
    });
    
    document.getElementById('encrypted-img-input').addEventListener('change', function(e) {
        previewImage(e, 'input-img');
    });
    
    document.getElementById('key-input').addEventListener('change', function(e) {
        previewText(e, 'crypto-key');
    });
    
    // Downloads
    document.getElementById('download-image-btn').addEventListener('click', function() {
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const fileName = currentMode === 'encrypt' ? `encrypted_${timestamp}.png` : `decrypted_${timestamp}.png`;
        downloadImage('output-img', fileName);
    });
    
    document.getElementById('download-key-btn').addEventListener('click', function() {
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        downloadKey('crypto-key', `key_${timestamp}.txt`);
    });
    
    // Modal
    document.getElementById('info-btn').addEventListener('click', function() {
        elements.infoModal.style.display = 'flex';
    });
    
    document.getElementById('close-modal').addEventListener('click', function() {
        elements.infoModal.style.display = 'none';
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === elements.infoModal) {
            elements.infoModal.style.display = 'none';
        }
    });
    
    // Parameter validation
    elements.alphaInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        if (value < 1) this.value = 1;
        if (value > 16) this.value = 16;
    });
    
    elements.iterInput.addEventListener('input', function() {
        const value = parseInt(this.value);
        if (value < 1) this.value = 1;
        if (value > 50) this.value = 50;
    });
    
    // Image overlay clicks
    document.getElementById('input-overlay').addEventListener('click', function() {
        if (currentMode === 'encrypt') {
            document.getElementById('img-input').click();
        } else {
            document.getElementById('encrypted-img-input').click();
        }
    });
    
    // Initialize
    switchMode('encrypt');
});

// Expose functions for PyScript
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.updateProgress = updateProgress;
window.showStatus = showStatus;
window.validateInputs = validateInputs;
window.updateImageInfo = updateImageInfo;
window.currentMode = () => currentMode;


