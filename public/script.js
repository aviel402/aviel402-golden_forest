// קובץ: public/script.js
// הגרסה היציבה והסופית של קוד הממשק

// נוודא שהקוד ירוץ רק אחרי שכל הדף נטען במלואו
document.addEventListener('DOMContentLoaded', () => {

    // איתור כל האלמנטים שאנו צריכים פעם אחת בלבד
    const loginView = document.getElementById('loginView');
    const registerView = document.getElementById('registerView');
    const showRegisterLink = document.getElementById('showRegister');
    const showLoginLink = document.getElementById('showLogin');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageElement = document.getElementById('message');

    // מאזין למעבר ממסך כניסה למסך הרשמה
    showRegisterLink.addEventListener('click', (event) => {
        event.preventDefault(); // מונע מהדף לקפוץ
        loginView.classList.add('hidden');
        registerView.classList.remove('hidden');
        messageElement.textContent = ''; // מנקה הודעות קודמות
    });

    // מאזין למעבר ממסך הרשמה בחזרה למסך כניסה
    showLoginLink.addEventListener('click', (event) => {
        event.preventDefault();
        registerView.classList.add('hidden');
        loginView.classList.remove('hidden');
        messageElement.textContent = '';
    });

    // מאזין לשליחת טופס ההרשמה
    registerForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        handleApiRequest('/api/register', { email, password }, 'יוצר שחקן חדש, אנא המתן...');
    });

    // מאזין לשליחת טופס הכניסה
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        handleApiRequest('/api/login', { email, password }, 'מאמת פרטים מול השרת...');
    });

    // פונקציית עזר מרכזית, המטפלת בכל התקשורת עם השרת
    async function handleApiRequest(endpoint, bodyData, loadingMessage) {
        
        messageElement.textContent = loadingMessage;
        messageElement.style.color = 'inherit'; // איפוס צבע ההודעה

        try {
            // שליחת הבקשה לשרת
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(bodyData)
            });

            // קבלת התשובה מהשרת
            const result = await response.json();

            // בדיקה אם השרת החזיר שגיאה (לדוגמה: 401, 409, 500)
            if (!response.ok) {
                throw new Error(result.error || 'אירעה שגיאה לא צפויה');
            }

            // אם הפעולה הצליחה, נציג הודעה ירוקה
            messageElement.style.color = 'green';
            messageElement.textContent = result.message;
            
            // אם זו הייתה כניסה מוצלחת, נשמור את הפרטים ונעבור לדף המשחק
            if (endpoint === '/api/login' && result.player_id) {
                // שומרים את מזהה השחקן בזיכרון המקומי של הדפדפן
                localStorage.setItem('player_id', result.player_id);
                
                setTimeout(() => {
                    // מעבר לדף המשחק
                    window.location.href = '/game.html';
                }, 1000); // נותנים למשתמש שנייה לקרוא את הודעת ההצלחה
            }

        } catch (error) {
            // במקרה של שגיאה, נציג אותה באדום
            messageElement.style.color = 'red';
            messageElement.textContent = `שגיאה: ${error.message}`;
        }
    }
});
```בעזרת השם יתברך, עכשיו, כשגם השרת וגם קוד הממשק מיושרים ותקינים, המערכת תעבוד. ישר כוח על הסבלנות.
