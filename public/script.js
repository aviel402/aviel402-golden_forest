document.addEventListener('DOMContentLoaded', () => {
    // ... כל הגדרות האלמנטים נשארות זהות ...
    const loginView = document.getElementById('loginView'), registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister'), showLoginLink = document.getElementById('showLogin');

    showRegisterLink.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
    showLoginLink.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });

    // טיפול בטופס ההרשמה
    document.getElementById('registerForm').addEventListener('submit', e => {
        e.preventDefault();
        // שינוי: קוראים את הערכים מהשדות הנכונים
        const username = document.getElementById('registerUsername').value;
        const password = document.getElementById('registerPassword').value;
        // שינוי: שולחים username במקום email
        handleApiRequest('/api/register', { username, password }, 'יוצר שחקן חדש...');
    });
    
    // טיפול בטופס הכניסה
    document.getElementById('loginForm').addEventListener('submit', e => {
        e.preventDefault();
        // שינוי: קוראים את הערכים מהשדות הנכונים
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        // שינוי: שולחים username במקום email
        handleApiRequest('/api/login', { username, password }, 'מנסה להתחבר...');
    });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        // פונקציית העזר נשארת כמעט זהה
        const messageEl = document.getElementById('message');
        messageEl.textContent = loadingMessage; messageEl.style.color = 'inherit';
        try {
            const response = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(bodyData) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'שגיאה לא צפויה');
            messageEl.style.color = 'green';
            messageEl.textContent = result.message;
            if (endpoint === '/api/login' && result.player_data) { 
                localStorage.setItem('player_data', JSON.stringify(result.player_data)); 
                setTimeout(() => { window.location.href = '/game.html'; }, 1000); 
            }
        } catch (error) {
            messageEl.style.color = 'red';
            messageEl.textContent = `שגיאה: ${error.message}`;
        }
    }
});
