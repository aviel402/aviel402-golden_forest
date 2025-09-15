// קובץ: public/game-script.js
// הגרסה המלאה והמתוקנת של קוד המשחק

document.addEventListener('DOMContentLoaded', () => {
    // --- איתור כל האלמנטים בדף ---
    const townView = document.getElementById('town-view');
    const combatView = document.getElementById('combat-view');
    const adventureBtn = document.getElementById('adventureBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const attackBtn = document.getElementById('attackBtn');
    
    // --- טעינת נתוני השחקן מהזיכרון ---
    let playerData = JSON.parse(localStorage.getItem('playerData'));
    if (!playerData) {
        // אם השחקן לא מחובר, אין מה לחפש כאן
        window.location.href = '/index.html';
        return;
    }

    // --- פונקציה לעדכון התצוגה של העיירה ---
    function updateTownUI(data) {
        playerData = data; // מעדכנים את המידע הגלובלי שלנו
        townView.classList.remove('hidden');
        combatView.classList.add('hidden');
        
        document.getElementById('player-username-town').textContent = data.username;
        document.getElementById('level').textContent = data.level;
        document.getElementById('xp').textContent = data.xp;
        document.getElementById('gold').textContent = data.gold;
        document.getElementById('health-town').textContent = data.health;
    }
    
    // --- פונקציה למעבר למסך הקרב ---
    function showCombatView(monster, message) {
        townView.classList.add('hidden');
        combatView.classList.remove('hidden');

        document.getElementById('player-username-combat').textContent = playerData.username;
        document.getElementById('player-health').textContent = playerData.health;
        document.getElementById('monster-name').textContent = monster.name;
        document.getElementById('monster-health').textContent = monster.health;
        document.getElementById('combat-message').textContent = message;
    }
    
    // --- הוספת מאזינים לכפתורים ---
    
    // כפתור התנתקות
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('playerData');
        window.location.href = '/index.html';
    });

    // כפתור יציאה להרפתקה
    adventureBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/adventure/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: playerData.username })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            showCombatView(result.monster, result.message);
        } catch (error) { alert(`שגיאה: ${error.message}`); }
    });
    
    // כפתור התקפה
    attackBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/combat/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: playerData.username, action: 'attack' })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            
            // תיקון ויזואלי: הצגת היומן עם נקודה ורווח
            document.getElementById('combat-message').textContent = result.log.join('. ');
            
            // עדכון המידע על המסך לפי התוצאה מהשרת
            if (result.player_data) {
                document.getElementById('player-health').textContent = result.player_data.health;
            }
            if (result.monster_data) {
                document.getElementById('monster-health').textContent = result.monster_data.health;
            }

            // אם הקרב הסתיים
            if (result.combat_over) {
                // נעדכן את המידע העדכני של השחקן (שנשלח מהשרת)
                localStorage.setItem('playerData', JSON.stringify(result.player_data));
                
                // נחכה 3 שניות כדי שהשחקן יקרא את ההודעה, ואז נחזור לעיירה
                setTimeout(() => {
                    updateTownUI(result.player_data);
                }, 3000);
            }
        } catch (error) {
             alert(`שגיאה בקרב: ${error.message}`);
             // אם הייתה תקלה בקרב, נחזיר לעיירה כדי למנוע מצב תקוע
             updateTownUI(playerData);
        }
    });

    // --- הפעלה ראשונית: הצגת נתוני העיירה כשהדף עולה ---
    updateTownUI(playerData);
});
