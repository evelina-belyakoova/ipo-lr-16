console.log('[JS] main.js запущен');

function getCSRFToken() {
    const name = 'csrftoken=';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name)) return c.substring(name.length);
    }
    return null;
}

function showToast(msg, type) {
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
            <div class="d-flex"><div class="toast-body">${msg}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>
        </div>`);
    const el = document.getElementById(id);
    new bootstrap.Toast(el, { delay: 3000 }).show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
}

function updateBadge() {
    const b = document.querySelector('.cart-count-badge');
    if (!b) return console.warn('[Badge] не найден');
    
    let current = b.textContent.trim();
    let n = parseInt(current, 10);
    if (isNaN(n)) n = 0;  
    
    b.textContent = n + 1;
    b.style.display = 'inline-flex';
    console.log('[Badge] ->', n + 1);
}

async function addToCart(id, name) {
    console.log('[Click] ID:', id, 'Name:', name);
    const token = getCSRFToken();
    
    try {
        const r = await fetch(`/api/cart/add/${id}/`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': token 
            },
            body: JSON.stringify({ quantity: 1 })
        });
        
        if (r.ok) {
            
            showToast( name + ' в корзине', 'success');
            updateBadge();
        } else {
            showToast('Ошибка API', 'error');
        }
    } catch(e) {
        showToast('Ошибка сети', 'error');
        console.error(e);
    }
}

window.testCart = () => addToCart(1, 'Тестовый товар');

document.addEventListener('DOMContentLoaded', () => {
    console.log('[JS] DOM готов');
    
    const buttons = document.querySelectorAll('.add-to-cart-btn');
    console.log(`[JS] Найдено кнопок: ${buttons.length}`);
    
    buttons.forEach((btn, index) => {
        console.log(`[JS] Привязываю клик к кнопке #${index + 1}`);
        
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            
            console.log('[Click] Клик пойман!');
            
            const id = btn.dataset.productId;
            const name = btn.dataset.productName;
            
            console.log('[Click] ID:', id, 'Name:', name);
            
            if (!id || !name) {
                console.error('[Click] Нет data-атрибутов!');
                return;
            }
            
            addToCart(id, name);
        });
    });
    
    window.testCart = function() {
        console.log('[Test] Запуск testCart()');
        const btn = document.querySelector('.add-to-cart-btn');
        if (btn) btn.click();
    };
});