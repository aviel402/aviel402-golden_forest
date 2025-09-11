// קובץ: public/game-script.js (מעודכן עם לוגיקת קרב)

document.addEventListener('DOMContentLoaded', async () => {
    
    // --- איתור כל האלמנטים בדף ---
    const townView = document.getElementById('town-view');
    const combatView = document.getElementById('combat-view');
    const adventureBtn = document.getElementById('adventureBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const attackBtn = document.getElementById('attackBtn');
    
    // --- טעינת נתוני השחקן מהזיכרון ---
    const playerData = JSON.parse(localStorage.getItem('playerData'));
    if (!playerData) { window.location.href = '/index.html'; return; }

    // --- אתחול והצגת נתוני השחקן ב"עיירה" ---
    function initializeTownView() {
        townView.classList.remove('hidden');
        combatView.classList.add('hidden');
        // נרענן את הנתונים מהשרת למקרה שעלו ברמה
        document.getElementById('player-username-town').textContent = playerData.username;
        document.getElementById('level').textContent = playerData.level || 1;
        document.getElementById('xp').textContent = playerData.xp || 0;
        document.getElementById('gold').textContent = playerData.gold || 0;
    }

    // --- פונקציה למעבר למצב קרב ---
    function showCombatView(monsterData, combatMessage) {
        townView.classList.add('hidden');
        combatView.classList.remove('hidden');

        document.getElementById('monster-name').textContent = monsterData.name;
        document.getElementById('monster-health').textContent = monsterData.health;
        document.getElementById('player-health').textContent = playerData.health || 100; // ברירת מחדל
        document.getElementById('combat-message').textContent = combatMessage;
    }
    
    // --- הוספת מאזינים לכפתורים ---
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('playerData');
        window.location.href = '/index.html';
    });

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

    // --- כאן נמצאת הלוגיקה החדשה של התקיפה ---
    attackBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/combat/action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: playerData.username, action: 'attack' })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            
            // עדכון המידע על המסך לפי התוצאה מהשרת
            document.getElementById('combat-message').textContent = result.log.join(' ');
            if(result.player_data) document.getElementById('player-health').textContent = result.player_data.health;
            if(result.monster_data) document.getElementById('monster-health').textContent = result.monster_data.health;

            // אם הקרב נגמר
            if (result.combat_over) {
                // נחכה 3 שניות כדי שהשחקן יקרא את ההודעה, ואז נחזור לעיירה
                setTimeout(() => {
                    // נעדכן את הנתונים של השחקן עם המידע העדכני (XP וזהב)
                    localStorage.setItem('playerData', JSON.stringify(result.player_data));
                    initializeTownView();
                }, 3000);
            }
        } catch (error) { alert(`שגיאה בקרב: ${error.message}`); }
    });

    // --- הפעלה ראשונית ---
    initializeTownView();
});