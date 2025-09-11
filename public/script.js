// קובץ: public/script.js
document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    
    showRegisterLink.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
    showLoginLink.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });
    
    document.getElementById('registerForm').addEventListener('submit', e => {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        handleApiRequest('/api/register', { username, password }, 'יוצר שחקן...');
    });
    
    document.getElementById('loginForm').addEventListener('submit', e => {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        handleApiRequest('/api/login', { username, password }, 'מתחבר...');
    });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = loadingMessage; messageEl.style.color = 'inherit';
        try {
            const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(bodyData) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'שגיאה לא צפויה');
            
            messageEl.style.color = 'green';
            messageEl.textContent = result.message;

            // --- זה החלק החשוב ---
            if (endpoint === '/api/login' && result.player_data) {
                // שומרים את הנתונים בזיכרון של הדפדפן
                localStorage.setItem('playerData', JSON.stringify(result.player_data)); 
                // מחכים שנייה ואז עוברים לדף המשחק
                setTimeout(() => { window.location.href = '/game.html'; }, 1000); 
            }
        } catch (error) {
            messageEl.style.color = 'red';
            messageEl.textContent = `שגיאה: ${error.message}`;
        }
    }
});