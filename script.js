// Working Payment System
function showCryptoPayment(service, amount) {
    const modal = document.getElementById('cryptoModal');
    const serviceNames = {
        'consultation': 'Security Consultation',
        'pentest': 'Penetration Testing', 
        'tools': 'Custom Tool Development'
    };
    
    document.getElementById('cryptoService').textContent = serviceNames[service];
    document.getElementById('cryptoAmount').textContent = amount;
    modal.style.display = 'block';
    
    // Show payment confirmation
    showNotification('Opening Bitcoin payment details...', 'success');
}

function closeCryptoModal() {
    document.getElementById('cryptoModal').style.display = 'none';
}

function copyAddress() {
    const address = document.getElementById('btcAddress').textContent;
    navigator.clipboard.writeText(address).then(function() {
        showNotification('✅ Bitcoin address copied to clipboard!', 'success');
    }).catch(function() {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = address;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('✅ Bitcoin address copied!', 'success');
    });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('cryptoModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Add payment tracking
document.addEventListener('DOMContentLoaded', function() {
    // Track CashApp clicks
    document.querySelectorAll('.cashapp').forEach(btn => {
        btn.addEventListener('click', function() {
            showNotification('🚀 Opening CashApp for payment...', 'success');
        });
    });
    
    // Track email clicks
    document.querySelectorAll('.email').forEach(btn => {
        btn.addEventListener('click', function() {
            showNotification('📧 Opening email client...', 'info');
        });
    });
});

// Threat map animation (existing code)
document.addEventListener('DOMContentLoaded', function() {
    const threatMap = document.querySelector('.threat-map');
    if (threatMap) {
        setInterval(() => {
            createThreatIndicator();
        }, 2000);
    }
});

function createThreatIndicator() {
    const threatMap = document.querySelector('.threat-map');
    if (!threatMap) return;
    
    const indicator = document.createElement('div');
    indicator.className = 'threat-indicator';
    indicator.style.left = Math.random() * 90 + '%';
    indicator.style.top = Math.random() * 90 + '%';
    
    threatMap.appendChild(indicator);
    
    setTimeout(() => {
        if (indicator.parentElement) {
            indicator.remove();
        }
    }, 4000);
}

function sendContactEmail(event) {
    event.preventDefault();
    
    const name = document.getElementById('clientName').value;
    const email = document.getElementById('clientEmail').value;
    const service = document.getElementById('serviceType').value;
    const budget = document.getElementById('budget').value;
    const details = document.getElementById('projectDetails').value;
    
    const serviceNames = {
        'consultation': 'Security Consultation ($100)',
        'pentest': 'Penetration Testing ($1000)',
        'custom-tool': 'Custom Tool Development ($500)',
        'other': 'Other Service'
    };
    
    const subject = `New Client Inquiry - ${serviceNames[service] || 'Cybersecurity Services'}`;
    const body = `Hi DeathSec333,

New client inquiry from your website:

CLIENT DETAILS:
Name: ${name}
Email: ${email}
Service: ${serviceNames[service] || service}
Budget: ${budget || 'Not specified'}

PROJECT DETAILS:
${details}

Please respond within 24 hours.

Best regards,
${name}`;
    
    const mailtoLink = `mailto:deathsec333@proton.me?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoLink;
    
    showNotification('📧 Email client opening with your message!', 'success');
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('cryptoModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
