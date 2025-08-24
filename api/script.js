// מחכים שכל הדף ייטען לפני שמפעילים את הקוד
document.addEventListener('DOMContentLoaded', function() {
    
    // מאתרים את האלמנטים החשובים בדף
    const registerForm = document.getElementById('registerForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const messageElement = document.getElementById('message');

    // מאזינים לאירוע "שליחה" של הטופס
    registerForm.addEventListener('submit', async function(event) {
        // מונעים מהדף להיטען מחדש באופן אוטומטי
        event.preventDefault();

        // אוספים את הערכים שהמשתמש הזין
        const email = emailInput.value;
        const password = passwordInput.value;

        // מנקים את הודעת השגיאה הקודמת ומציגים הודעת טעינה
        messageElement.textContent = 'יוצר שחקן חדש...';
        messageElement.style.color = '#333';

        try {
            // שולחים את הנתונים לשרת הפייתון שלנו ב-Vercel
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email, password: password })
            });

            // ממתינים לתשובה מהשרת
            const result = await response.json();

            // אם השרת החזיר תשובה שאינה הצלחה (למשל, שגיאת 409)
            if (!response.ok) {
                // נזרוק שגיאה עם ההודעה שהגיעה מהשרת
                throw new Error(result.error || 'אירעה שגיאה לא צפויה');
            }

            // אם הגענו לכאן, ההרשמה הצליחה!
            messageElement.style.color = 'green';
            messageElement.textContent = `נרשמת בהצלחה! השחקן שלך נוצר.`;

        } catch (error) {
            // אם הייתה בעיה כלשהי במהלך התהליך (בתקשורת או בשרת)
            messageElement.style.color = 'red';
            messageElement.textContent = 'שגיאה: ' + error.message;
        }
    });

});