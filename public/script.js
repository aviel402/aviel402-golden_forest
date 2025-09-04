document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');
    
    if (showRegister) showRegister.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
    if (showLogin) showLogin.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });
    
    if(document.getElementById('registerForm')) document.getElementById('registerForm').addEventListener('submit', e => { e.preventDefault(); handleApiRequest('/api/register', { email: document.getElementById('registerEmail').value, password: document.getElementById('registerPassword').value }, 'יוצר שחקן...'); });
    if(document.getElementById('loginForm')) document.getElementById('loginForm').addEventListener('submit', e => { e.preventDefault(); handleApiRequest('/api/login', { email: document.getElementById('loginEmail').value, password: document.getElementById('loginPassword').value }, 'מתחבר...'); });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = loadingMessage; messageEl.style.color = 'inherit';
        try {
            const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(bodyData) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'שגיאה לא צפויה');
            messageEl.style.color = 'green';
            messageEl.textContent = result.message;
            if (endpoint === '/api/login' && result.player_id) { localStorage.setItem('player_id', result.player_id); setTimeout(() => { window.location.href = '/game.html'; }, 1000); }
        } catch (error) { messageEl.style.color = 'red'; messageEl.textContent = `שגיאה: ${error.message}`; }
    }
});
