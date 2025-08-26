// קובץ: public/script.js - גרסה מתוקנת ובדוקה

// הפונקציה המרכזית תופעל רק אחרי שכל תוכן הדף נטען
document.addEventListener('DOMContentLoaded', () => {

    // איתור כל האלמנטים פעם אחת ושמירתם במשתנים
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageElement = document.getElementById('message');

    // ודא שכל האלמנטים אכן נמצאו לפני שנמשיך
    if (!loginView || !registerView || !showRegisterLink || !showLoginLink || !loginForm || !registerForm || !messageElement) {
        console.error('שגיאה קריטית: אחד מאלמנטי ה-HTML לא נמצא בדף.');
        return; // עוצרים את ריצת הקוד אם יש בעיה
    }

    // מאזין שמטפל במעבר להרשמה
    showRegisterLink.addEventListener('click', (event) => {
        event.preventDefault(); // מונע מהקישור לקפוץ
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
        messageElement.textContent = ''; // מנקה הודעות
    });

    // מאזין שמטפל בחזרה לכניסה
    showLoginLink.addEventListener('click', (event) => {
        event.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
        messageElement.textContent = '';
    });

    // מאזין ללחיצה על כפתור ההרשמה
    registerForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        // קריאה לפונקציה המרכזית שתשלח את הבקשה לשרת
        handleApiRequest('/api/register', { email, password }, 'יוצר שחקן...');
    });

    // מאזין ללחיצה על כפתור הכניסה
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        handleApiRequest('/api/login', { email, password }, 'מתחבר למשחק...');
    });

    // פונקציית עזר מרכזית לטיפול בכל הבקשות לשרת
    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        messageElement.textContent = loadingMessage;
        messageElement.style.color = 'inherit'; // איפוס צבע

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bodyData)
            });

            const result = await response.json();

            if (!response.ok) {
                // אם השרת החזיר שגיאה (למשל, 409 - משתמש קיים)
                throw new Error(result.error || `HTTP error! status: ${response.status}`);
            }

            // הצלחה
            messageElement.style.color = 'green';
            messageElement.textContent = result.message;

            // אחרי כניסה מוצלחת, בעתיד נעבור למסך המשחק
            if (endpoint === '/api/login' && result.player_id) {
                setTimeout(() => {
                    // כאן נוסיף את המעבר לדף המשחק
                    console.log(`התחברת בהצלחה! מזהה שחקן: ${result.player_id}. כעת נעביר אותך למשחק...`);
                    // window.location.href = '/game.html';
                }, 1500); // ממתינים שנייה וחצי ורק אז מעבירים
            }

        } catch (error) {
            messageElement.style.color = 'red';
            messageElement.textContent = `שגיאה: ${error.message}`;
        }
    }
});
