// DeathSec333 Website Security Warning System
(function() {
    'use strict';
    
    // Detect suspicious activity
    let suspiciousActivity = false;
    let warningShown = false;
    
    // Monitor for common attack patterns
    const suspiciousPatterns = [
        'script', 'alert', 'eval', 'document.cookie',
        'javascript:', 'vbscript:', 'onload', 'onerror',
        '../', '..\\', 'etc/passwd', 'cmd.exe'
    ];
    
    // Check URL for suspicious content
    function checkURL() {
        const url = window.location.href.toLowerCase();
        return suspiciousPatterns.some(pattern => url.includes(pattern));
    }
    
    // Check for developer tools (F12)
    function detectDevTools() {
        const threshold = 160;
        if (window.outerHeight - window.innerHeight > threshold || 
            window.outerWidth - window.innerWidth > threshold) {
            return true;
        }
        return false;
    }
    
    // Show security warning
    function showSecurityWarning() {
        if (warningShown) return;
        warningShown = true;
        
        // Get visitor IP (approximate)
        fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {
                const userIP = data.ip;
                showWarningModal(userIP);
            })
            .catch(() => {
                showWarningModal('Unknown');
            });
    }
    
    function showWarningModal(ip) {
        // Create warning overlay
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            z-index: 999999;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Courier New', monospace;
        `;
        
        // Create warning box
        const warningBox = document.createElement('div');
        warningBox.style.cssText = `
            background: linear-gradient(45deg, #ff0040, #cc0033);
            border: 3px solid #fff;
            border-radius: 15px;
            padding: 40px;
            max-width: 600px;
            text-align: center;
            color: white;
            box-shadow: 0 0 50px rgba(255, 0, 64, 0.8);
            animation: pulse 2s infinite;
        `;
        
        warningBox.innerHTML = `
            <div style="font-size: 3em; margin-bottom: 20px;">⚠️ SECURITY ALERT ⚠️</div>
            <div style="font-size: 1.5em; margin-bottom: 20px; color: #ffff00;">
                UNAUTHORIZED ACCESS ATTEMPT DETECTED
            </div>
            <div style="font-size: 1.2em; margin-bottom: 30px;">
                <strong>Your IP Address: ${ip}</strong><br>
                <strong>Timestamp: ${new Date().toLocaleString()}</strong><br>
                <strong>Location: Logged and Tracked</strong>
            </div>
            <div style="font-size: 1em; margin-bottom: 30px; line-height: 1.6;">
                🚨 <strong>WARNING:</strong> Attempting to hack, exploit, or gain unauthorized access 
                to this website is a federal crime under:<br><br>
                • Computer Fraud and Abuse Act (CFAA)<br>
                • Digital Millennium Copyright Act (DMCA)<br>
                • State and Federal Cybercrime Laws<br><br>
                <strong style="color: #ffff00;">All activities are monitored, logged, and reported to authorities.</strong>
            </div>
            <div style="font-size: 1.1em; margin-bottom: 30px; color: #00ff00;">
                This is a professional cybersecurity website.<br>
                Legitimate visitors are welcome.
            </div>
            <button id="acknowledgeBtn" style="
                background: #00ff00;
                color: #000;
                border: none;
                padding: 15px 30px;
                font-size: 1.2em;
                font-weight: bold;
                border-radius: 25px;
                cursor: pointer;
                margin: 10px;
            ">I UNDERSTAND - CONTINUE</button>
            <div style="font-size: 0.9em; margin-top: 20px; color: #ccc;">
                DeathSec333 Professional Cybersecurity<br>
                Protected by advanced security monitoring
            </div>
        `;
        
        // Add CSS animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
        `;
        document.head.appendChild(style);
        
        overlay.appendChild(warningBox);
        document.body.appendChild(overlay);
        
        // Handle acknowledge button
        document.getElementById('acknowledgeBtn').onclick = function() {
            overlay.remove();
            // Log the acknowledgment
            console.log(`Security warning acknowledged by IP: ${ip}`);
        };
        
        // Log the security event
        logSecurityEvent(ip);
    }
    
    function logSecurityEvent(ip) {
        // Log to console (you can extend this to send to your server)
        console.log(`🚨 SECURITY ALERT: Suspicious activity detected from IP: ${ip} at ${new Date()}`);
        
        // Optional: Send to your logging endpoint
        // fetch('/log-security-event', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ ip, timestamp: new Date(), type: 'suspicious_activity' })
        // });
    }
    
    // Monitor for suspicious activity
    function monitorSecurity() {
        // Check URL for suspicious patterns
        if (checkURL()) {
            suspiciousActivity = true;
        }
        
        // Check for developer tools
        if (detectDevTools()) {
            suspiciousActivity = true;
        }
        
        // Show warning if suspicious activity detected
        if (suspiciousActivity && !warningShown) {
            showSecurityWarning();
        }
    }
    
    // Start monitoring
    setInterval(monitorSecurity, 1000);
    
    // Also check on page load
    window.addEventListener('load', monitorSecurity);
    
    // Disable right-click context menu
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        showSecurityWarning();
    });
    
    // Disable F12, Ctrl+Shift+I, Ctrl+U
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F12' || 
            (e.ctrlKey && e.shiftKey && e.key === 'I') ||
            (e.ctrlKey && e.key === 'u')) {
            e.preventDefault();
            showSecurityWarning();
        }
    });
    
})();
