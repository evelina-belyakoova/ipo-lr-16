
function getCSRFToken() {
    const name = 'csrftoken=';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name)) {
            return c.substring(name.length);
        }
    }
    return null;
}

function showToast(msg, type = 'success') {
    let box = document.getElementById('toast-box');
    if (!box) {
        box = document.createElement('div');
        box.id = 'toast-box';
        box.className = 'toast-container position-fixed top-0 end-0 p-3';
        box.style.zIndex = '1100';
        document.body.appendChild(box);
    }
    const id = 't-' + Date.now();
    const bg = type === 'success' ? 'bg-success' : 'bg-danger';
    box.insertAdjacentHTML('beforeend', `
        <div id="${id}" class="toast align-items-center text-white ${bg} border-0">
            <div class="d-flex">
                <div class="toast-body">${msg}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast"></button>
            </div>
        </div>`);
    const el = document.getElementById(id);
    if (typeof bootstrap !== 'undefined') {
        new bootstrap.Toast(el, { delay: 3000 }).show();
        el.addEventListener('hidden.bs.toast', () => el.remove());
    } else {
        setTimeout(() => el.remove(), 3000);
    }
}

function updateBadge() {
    const badge = document.getElementById('cart-badge');
    if (!badge) return;
    
    fetch('/cart/', { credentials: 'same-origin' })
        .then(r => r.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newBadge = doc.getElementById('cart-badge');
            if (newBadge) {
                badge.textContent = newBadge.textContent;
            }
        })
        .catch(err => console.error('[Badge] Ошибка:', err));
}

async function addToCart(productId, productName) {
    console.log('[Cart] Добавление:', productId, productName);
    
    try {
        const response = await fetch(`/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'same-origin',
            redirect: 'follow'
        });
        
        console.log('[Cart] Статус:', response.status);
        
        if (response.ok || response.redirected) {
            showToast('✅ ' + productName + ' добавлен в корзину', 'success');
            updateBadge();
        } else if (response.status === 401 || response.status === 302) {
            window.location.href = '/accounts/login/?next=' + encodeURIComponent(window.location.pathname);
        } else {
            showToast('❌ Ошибка при добавлении (статус ' + response.status + ')', 'error');
        }
    } catch (error) {
        console.error('[Cart] Ошибка сети:', error);
        showToast('❌ Ошибка сети: ' + error.message, 'error');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('[Main] Скрипт загружен');
    
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const productName = this.dataset.productName || 'Товар';
            addToCart(productId, productName);
        });
    });
    
    updateBadge();
});

window.addToCart = addToCart;
window.showToast = showToast;
window.updateBadge = updateBadge;