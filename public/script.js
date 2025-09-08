document.addEventListener('DOMContentLoaded', () => {
const loginView = document.getElementById('loginView');
const registerView = document.getElementById('registerView');
const showRegisterLink = document.getElementById('showRegister');
const showLoginLink = document.getElementById('showLogin');
showRegisterLink.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
showLoginLink.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });

document.getElementById('registerForm').addEventListener('submit', e => {
    e.preventDefault();
    handleApiRequest('/api/register', { 
        username: document.getElementById('registerUsername').value, 
        password: document.getElementById('registerPassword').value 
    }, 'יוצר שחקן...');
});

document.getElementById('loginForm').addEventListener('submit', e => {
    e.preventDefault();
    handleApiRequest('/api/login', { 
        username: document.getElementById('loginUsername').value, 
        password: document.getElementById('loginPassword').value 
    }, 'מתחבר...');
});

async function handleApiRequest(endpoint, bodyData, loadingMessage) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = loadingMessage;
    messageEl.style.color = 'inherit';
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(bodyData)
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || 'שגיאה לא צפויה');
        
        messageEl.style.color = 'green';
        messageEl.textContent = result.message;
        
        // --- התיקון הקריטי כאן ---
        // אנחנו בודקים אם השרת החזיר אובייקט 'player_data'
        if (endpoint === '/api/login' && result.player_data) {
            // שומרים את כל המידע על השחקן, לא רק את ה-ID
            localStorage.setItem('player_data', JSON.stringify(result.player_data)); 
            setTimeout(() => { 
                window.location.href = '/game.html'; 
            }, 1000); 
        }
    } catch (error) {
        messageEl.style.color = 'red';
        messageEl.textContent = `שגיאה: ${error.message}`;
    }
}
});
