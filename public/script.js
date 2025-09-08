// קובץ: public/script.js - גרסת בדיקה פשוטה

// הדבר הראשון שהקובץ עושה, כדי שנדע שהוא נטען
console.log("בדיקה: קובץ script.js נטען.");

// הקוד ימתין עד שכל ה-HTML יהיה מוכן
document.addEventListener('DOMContentLoaded', () => {
    
    // נודיע שהשלב הזה עבר בהצלחה
    console.log("בדיקה: אירוע DOMContentLoaded הופעל. הדף מוכן.");

    // נאתר את שני הכפתורים החשובים
    const loginButton = document.querySelector('#loginForm button');
    const registerButton = document.getElementById('showRegister');
    
    // --- בדיקה עבור כפתור הכניסה ---
    if (loginButton) {
        console.log("בדיקה: כפתור 'היכנס ליער' נמצא בהצלחה!");
        
        loginButton.addEventListener('click', (event) => {
            event.preventDefault(); // מונעים מהטופס להישלח
            console.log("!!! הצלחה: כפתור הכניסה נלחץ והגיב !!!");
            alert('הצלחה! כפתור הכניסה עובד!');
        });
    } else {
        console.error("!!! שגיאה: כפתור 'היכנס ליער' לא נמצא בדף !!!");
    }

    // --- בדיקה עבור קישור ההרשמה ---
    if (registerButton) {
        console.log("בדיקה: הקישור 'הירשם כאן' נמצא בהצלחה!");
        
        registerButton.addEventListener('click', (event) => {
            event.preventDefault();
            console.log("!!! הצלחה: קישור ההרשמה נלחץ והגיב !!!");
            alert('הצלחה! הקישור להרשמה עובד!');
        });
    } else {
        console.error("!!! שגיאה: הקישור 'הירשם כאן' לא נמצא בדף !!!");
    }
});
