// קובץ: public/game-script.js - גרסת קרב פשוטה ובלי שרת

document.addEventListener('DOMContentLoaded', () => {
    
    // איתור אלמנטים
    const townView = document.getElementById('town-view');
    const combatView = document.getElementById('combat-view');
    const playerData = JSON.parse(localStorage.getItem('playerData')); // מידע בסיסי כמו שם משתמש
    
    if (!playerData) {
        window.location.href = '/index.html';
        return;
    }

    // --- הגדרת המשתנים של הקרב ---
    let currentPlayerHealth;
    let currentMonster;
    
    // --- ספר החיות שלנו (חי בתוך הדפדפן) ---
    const CREATURE_BOOK = [
        {name: 'עכבר שדה', health: 20, attack: 5},
        {name: 'עכביש יער', health: 25, attack: 7},
        {name: 'חזיר בר קטן', health: 40, attack: 10}
    ];

    // --- פונקציות שמנהלות את התצוגה ---
    function showTownView() {
        townView.classList.remove('hidden');
        combatView.classList.add('hidden');
        document.getElementById('player-username-town').textContent = playerData.username;
        // ... בעתיד נציג כאן נתונים מהשרת
    }

    function showCombatView(monster, message) {
        townView.classList.add('hidden');
        combatView.classList.remove('hidden');
        document.getElementById('player-username-combat').textContent = playerData.username;
        document.getElementById('monster-name').textContent = monster.name;
        updateCombatUI(message);
    }

    function updateCombatUI(message) {
        document.getElementById('player-health').textContent = currentPlayerHealth;
        document.getElementById('monster-health').textContent = currentMonster.health;
        document.getElementById('combat-message').textContent = message;
    }
    
    // --- הוספת מאזינים לכפתורים ---

    // כפתור יציאה להרפתקה - מתחיל קרב חדש
    document.getElementById('adventureBtn').addEventListener('click', () => {
        // מאתחלים קרב: שחקן עם 100 חיים, וחיה אקראית מהספר
        currentPlayerHealth = 100;
        currentMonster = { ...random.choice(CREATURE_BOOK) }; // העתקה של החיה כדי לא לשנות את המקור
        const message = `בשיטוט ביער, נתקלת ב: ${currentMonster.name}!`;
        showCombatView(currentMonster, message);
    });
    
    // כפתור התקפה
    document.getElementById('attackBtn').addEventListener('click', () => {
        if (currentPlayerHealth <= 0 || currentMonster.health <= 0) return; // הקרב כבר נגמר

        const playerAttack = 10; // נתון קבוע כרגע
        let combatMessage = '';

        // השחקן תוקף
        currentMonster.health -= playerAttack;
        combatMessage += `הנחתת מכה וגרמת ${playerAttack} נזק. `;

        // בודקים אם המפלצת הובסה
        if (currentMonster.health <= 0) {
            currentMonster.health = 0; // שלא יהיו חיים במינוס
            combatMessage += `הבסת את ${currentMonster.name}! לחץ 'חזור לעיירה' כדי לסיים.`;
            document.getElementById('attackBtn').textContent = "חזור לעיירה"; // משנים את הכפתור
            document.getElementById('attackBtn').onclick = showTownView; // לחיצה תחזיר לעיירה
            updateCombatUI(combatMessage);
            return;
        }

        // המפלצת תוקפת בחזרה
        currentPlayerHealth -= currentMonster.attack;
        combatMessage += `החיה תקפה וגרמה ${currentMonster.attack} נזק.`;

        // בודקים אם השחקן הובס
        if (currentPlayerHealth <= 0) {
            currentPlayerHealth = 0;
            combatMessage += ` הובסת בקרב... לחץ 'חזור לעיירה'.`;
            document.getElementById('attackBtn').textContent = "התחל מחדש";
            document.getElementById('attackBtn').onclick = showTownView;
        }

        updateCombatUI(combatMessage);
    });

    // כפתור התנתקות
    document.getElementById('logoutBtn').addEventListener('click', () => {
        localStorage.removeItem('playerData');
        window.location.href = '/index.html';
    });

    // --- הפעלה ראשונית ---
    // (פונקציה לבחירה אקראית)
    random.choice = function(arr) {
        return arr[Math.floor(Math.random() * arr.length)];
    }
    showTownView(); // מתחילים תמיד מהעיירה
});
