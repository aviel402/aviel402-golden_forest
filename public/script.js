// קובץ: public/script.js
// גרסה פשוטה וישירה המבוססת על העיקרון שהכתובת היא הדבר היחיד שמשתנה.

document.addEventListener('DOMContentLoaded', function() {

    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const messageElement = document.getElementById('message');
    
    // מעבר למסך הרשמה
    showRegisterLink.addEventListener('click', function(e) {
        e.preventDefault();
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
        messageElement.textContent = '';
    });
    
    // מעבר למסך כניסה
    showLoginLink.addEventListener('click', function(e) {
        e.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
        messageElement.textContent = '';
    });
    
    // =======================================================
    //          העיקרון המרכזי בפעולה
    // =======================================================

    // טיפול בטופס ההרשמה
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        // קוראים לפונקציה הראשית עם הכתובת הנכונה
        handleApiRequest('/api/register', { email, password }, 'יוצר שחקן חדש...');
    });
    
    // טיפול בטופס הכניסה
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        // קוראים לאותה פונקציה ראשית, רק עם כתובת שונה
        handleApiRequest('/api/login', { email, password }, 'מנסה להתחבר...');
    });

    // =======================================================
    //    פונקציית עזר כללית - נשארה זהה כי היא בנויה נכון
    // =======================================================
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
