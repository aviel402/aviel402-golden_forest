document.addEventListener('DOMContentLoaded', function() {
    
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageElement = document.getElementById('message');

    // מאזין למעבר להרשמה
    showRegisterLink.addEventListener('click', function(event) {
        event.preventDefault();
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
        messageElement.textContent = '';
    });

    // מאזין למעבר לכניסה
    showLoginLink.addEventListener('click', function(event) {
        event.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
        messageElement.textContent = '';
    });

    // טיפול בטופס הרשמה
    registerForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        handleApiRequest('/api/register', { email, password }, "יוצר שחקן חדש...");
    });

    // טיפול בטופס כניסה
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        handleApiRequest('/api/login', { email, password }, "מנסה להתחבר...");
    });
    
    // פונקציית עזר לשליחת בקשות
    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        messageElement.textContent = loadingMessage;
        messageElement.style.color = '#333';
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bodyData)
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.error || 'אירעה שגיאה לא צפויה');
            }
            messageElement.style.color = 'green';
            messageElement.textContent = result.message;

            // אחרי כניסה מוצלחת, בעתיד נעבור למסך המשחק
            if (endpoint === '/api/login') {
                console.log('Login successful for player ID:', result.player_id);
                // לדוגמה, בעתיד הקרוב נוסיף:
                // window.location.href = `/game.html?player_id=${result.player_id}`;
            }
            
        } catch (error) {
            messageElement.style.color = 'red';
            messageElement.textContent = 'שגיאה: ' + error.message;
        }
    }
});