const express = require('express');
const helmet = require('helmet');
const path = require('path');

const app = express();
const PORT = 1339;  // Different port since 1337 is taken

// Security middleware
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true
    }
}));

// Serve static files
app.use(express.static(__dirname));

// Custom security headers
app.use((req, res, next) => {
    res.setHeader('X-Powered-By', 'DeathSec333-Node-Professional');
    res.setHeader('Server', 'DeathSec333-Node-Secure');
    next();
});

// Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/tools', (req, res) => {
    res.sendFile(path.join(__dirname, 'tools_marketplace.html'));
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
    console.log(`🔥 DeathSec333 Node.js Server running on port ${PORT}`);
    console.log(`🌐 Local: http://localhost:${PORT}`);
    console.log(`🌐 Network: http://[YOUR_IP]:${PORT}`);
    console.log(`🔒 Node.js security headers enabled`);
    console.log(`🐍 Python server on port 1337`);
    console.log(`🟢 nginx also available`);
});
