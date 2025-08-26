document.addEventListener('DOMContentLoaded', () => {
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const messageElement = document.getElementById('message');
    
    showRegisterLink.addEventListener('click', (e) => {
        e.preventDefault();
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
        messageElement.textContent = '';
    });
    
    showLoginLink.addEventListener('click', (e) => {
        e.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
        messageElement.textContent = '';
    });
    
    document.getElementById('registerForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        handleApiRequest('/api/register', { email, password }, 'יוצר שחקן חדש...');
    });
    
    document.getElementById('loginForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        handleApiRequest('/api/login', { email, password }, 'מנסה להתחבר...');
    });

    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        messageElement.textContent = loadingMessage;
        messageElement.style.color = 'inherit';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bodyData)
            });
            const result = await response.json();
            if (!response.ok) { throw new Error(result.error || 'שגיאה לא צפויה'); }
            messageElement.style.color = 'green';
            messageElement.textContent = result.message;
        } catch (error) {
            messageElement.style.color = 'red';
            messageElement.textContent = `שגיאה: ${error.message}`;
        }
    }
});
