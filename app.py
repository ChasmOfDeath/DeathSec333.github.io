from flask import Flask, render_template, request, jsonify
import requests
import hashlib
import time
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Generate encryption key (store this securely in production)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Bitcoin payment configuration
BTC_ADDRESS = "your_btc_address_here"  # Replace with your actual BTC address

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-payment', methods=['POST'])
def generate_payment():
    """Generate Bitcoin payment address for order"""
    data = request.json
    product = data.get('product')
    amount_usd = data.get('amount')
    
    # Get current BTC price
    try:
        response = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC')
        btc_rate = float(response.json()['data']['rates']['USD'])
        btc_amount = round(amount_usd / btc_rate, 8)
    except:
        return jsonify({'error': 'Unable to fetch BTC rate'}), 500
    
    return jsonify({
        'btc_address': BTC_ADDRESS,
        'btc_amount': btc_amount,
        'usd_amount': amount_usd,
        'product': product
    })

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    """Verify Bitcoin payment"""
    data = request.json
    tx_hash = data.get('tx_hash')
    
    # Check transaction on blockchain
    try:
        response = requests.get(f'https://blockchain.info/rawtx/{tx_hash}')
        tx_data = response.json()
        
        # Verify transaction details
        for output in tx_data['out']:
            if output.get('addr') == BTC_ADDRESS:
                return jsonify({
                    'verified': True,
                    'amount': output['value'] / 100000000,  # Convert satoshis to BTC
                    'confirmations': tx_data.get('confirmations', 0)
                })
        
        return jsonify({'verified': False, 'error': 'Payment not found'})
    except:
        return jsonify({'verified': False, 'error': 'Unable to verify transaction'})

@app.route('/api/contact', methods=['POST'])
def contact():
    """Handle encrypted contact form"""
    data = request.json
    
    # Encrypt sensitive data
    encrypted_message = cipher_suite.encrypt(data.get('message').encode())
    encrypted_email = cipher_suite.encrypt(data.get('email').encode())
    
    # In production, save to database or send via secure channel
    # For now, just return success
    
    return jsonify({
        'success': True,
        'message': 'Your encrypted message has been received'
    })

@app.route('/api/products', methods=['GET'])
def get_products():
    """Return available products"""
    products = [
        {
            'id': 1,
            'name': 'Premium Exploit Kit',
            'price': 500,
            'description': 'Advanced exploitation framework',
            'category': 'tools'
        },
        {
            'id': 2,
            'name': 'Zero-Day Vulnerability',
            'price': 5000,
            'description': 'Unpatched security vulnerability',
            'category': 'exploits'
        },
        {
            'id': 3,
            'name': 'Penetration Testing Service',
            'price': 1000,
            'description': 'Professional security assessment',
            'category': 'services'
        }
    ]
    return jsonify(products)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
