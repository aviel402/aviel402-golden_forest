document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('loginView'), registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister'), showLoginLink = document.getElementById('showLogin');
    
    showRegisterLink.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
    showLoginLink.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });
    
    document.getElementById('registerForm').addEventListener('submit', e => { e.preventDefault(); handleApiRequest('/api/register', { email: document.getElementById('registerEmail').value, password: document.getElementById('registerPassword').value }, 'יוצר שחקן...'); });
    document.getElementById('loginForm').addEventListener('submit', e => { e.preventDefault(); handleApiRequest('/api/login', { email: document.getElementById('loginEmail').value, password: document.getElementById('loginPassword').value }, 'מתחבר...'); });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        const messageElement = document.getElementById('message');
        messageElement.textContent = loadingMessage; messageElement.style.color = 'inherit';
        try {
            const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(bodyData) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'שגיאה לא צפויה');
            messageElement.style.color = 'green';
            messageElement.textContent = result.message;
            if (endpoint === '/api/login' && result.player_id) { localStorage.setItem('player_id', result.player_id); setTimeout(() => { window.location.href = '/game.html'; }, 1000); }
        } catch (error) { messageElement.style.color = 'red'; messageElement.textContent = `שגיאה: ${error.message}`; }
    }
});