const API_URL = 'https://deathsec333-production.up.railway.app';

// Load products
async function loadProducts() {
    try {
        const response = await fetch(`${API_URL}/api/products`);
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Generate Bitcoin payment
async function buyProduct(productName, price) {
    try {
        const response = await fetch(`${API_URL}/api/generate-payment`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product: productName, amount: price })
        });
        const payment = await response.json();
        showPayment(payment);
    } catch (error) {
        console.error('Error:', error);
    }
}

// Display products
function displayProducts(products) {
    const container = document.getElementById('products') || document.body;
    products.forEach(p => {
        const div = document.createElement('div');
        div.className = 'product';
        div.innerHTML = `
            <h3>${p.name}</h3>
            <p>${p.description}</p>
            <p class="price">$${p.price}</p>
            <button onclick="buyProduct('${p.name}', ${p.price})">
                Buy with Bitcoin
            </button>
        `;
        container.appendChild(div);
    });
}

// Show payment details
function showPayment(payment) {
    alert(`Send ${payment.btc_amount} BTC to:\n${payment.btc_address}`);
}

// Auto-load on page ready
document.addEventListener('DOMContentLoaded', loadProducts);
