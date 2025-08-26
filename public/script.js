document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegister = document.getElementById('showRegister');
    const showLogin = document.getElementById('showLogin');
    
    showRegister.addEventListener('click', e => { e.preventDefault(); loginView.classList.add('hidden'); registerView.classList.remove('hidden'); });
    showLogin.addEventListener('click', e => { e.preventDefault(); registerView.classList.add('hidden'); loginView.classList.remove('hidden'); });
    
    document.getElementById('registerForm').addEventListener('submit', e => {
        e.preventDefault();
        handleApiRequest('/api/register', { email: document.getElementById('registerEmail').value, password: document.getElementById('registerPassword').value }, 'יוצר שחקן חדש...');
    });
    
    document.getElementById('loginForm').addEventListener('submit', e => {
        e.preventDefault();
        handleApiRequest('/api/login', { email: document.getElementById('loginEmail').value, password: document.getElementById('loginPassword').value }, 'מתחבר למשחק...');
    });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        const messageEl = document.getElementById('message');
        messageEl.textContent = loadingMessage; messageEl.style.color = 'inherit';
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
        } catch (error) {
            messageEl.style.color = 'red';
            messageEl.textContent = `שגיאה: ${error.message}`;
        }
    }
});
