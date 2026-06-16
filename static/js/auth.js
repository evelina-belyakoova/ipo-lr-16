
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

async function apiRequest(url, options = {}) {
    const needsCSRF = ['POST', 'PUT', 'PATCH', 'DELETE'].includes(
        (options.method || 'GET').toUpperCase()
    );

    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
    };

    if (needsCSRF) {
        const token = getCSRFToken();
        if (token) {
            headers['X-CSRFToken'] = token;
        } else {
            console.warn('[Auth] CSRF-токен не найден в cookie');
        }
    }

    try {
        const response = await fetch(url, {
            ...options,
            headers: headers,
            credentials: 'same-origin' 
        });

        if (response.status === 401) {
            console.warn('[Auth] 401: Требуется авторизация');
            const next = encodeURIComponent(window.location.pathname);
            window.location.href = `/accounts/login/?next=${next}`;
            throw new Error('Требуется авторизация');
        }

        if (response.status === 403) {
            console.error('[Auth] 403: Недостаточно прав');
            showToast('❌ Недостаточно прав для этого действия', 'error');
            throw new Error('Доступ запрещён');
        }

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`[Auth] HTTP ${response.status}:`, errorText);
            throw new Error(`HTTP ${response.status}`);
        }
        if (response.status === 204) {
            return null;
        }
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }

        return await response.text();

    } catch (error) {
        console.error('[Auth] Ошибка запроса:', error);
        throw error;
    }
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

window.apiRequest = apiRequest;
window.getCSRFToken = getCSRFToken;
window.showToast = showToast;

console.log('[Auth] Модуль авторизации загружен');