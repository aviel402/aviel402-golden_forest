document.addEventListener('DOMContentLoaded', () => {
    const townView = document.getElementById('town-view'), combatView = document.getElementById('combat-view');
    let playerData = JSON.parse(localStorage.getItem('playerData'));
    if (!playerData) { window.location.href = '/index.html'; return; }

    function updateTownUI(data) {
        townView.classList.remove('hidden'); combatView.classList.add('hidden');
        document.getElementById('player-username-town').textContent = data.username;
        document.getElementById('level').textContent = data.level; document.getElementById('xp').textContent = data.xp;
        document.getElementById('gold').textContent = data.gold; document.getElementById('health-town').textContent = data.health;
    }
    
    document.getElementById('adventureBtn').addEventListener('click', async () => {
        try {
            const response = await fetch('/api/adventure/start', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: playerData.username }) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            showCombatView(result.monster, result.message);
        } catch (error) { alert(`שגיאה: ${error.message}`); }
    });
    
    function showCombatView(monster, message) {
        townView.classList.add('hidden'); combatView.classList.remove('hidden');
        document.getElementById('player-username-combat').textContent = playerData.username;
        document.getElementById('player-health').textContent = playerData.health;
        document.getElementById('monster-name').textContent = monster.name;
        document.getElementById('monster-health').textContent = monster.health;
        document.getElementById('combat-message').textContent = message;
    }
    
    document.getElementById('attackBtn').addEventListener('click', async () => {
        try {
            const response = await fetch('/api/combat/action', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ username: playerData.username, action: 'attack' }) });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error);
            document.getElementById('combat-message').textContent = result.log.join(' \n ');
            if (result.player_data) { playerData = result.player_data; document.getElementById('player-health').textContent = playerData.health; }
            if (result.monster_data) document.getElementById('monster-health').textContent = result.monster_data.health;
            if (result.combat_over) {
                setTimeout(() => {
                    localStorage.setItem('playerData', JSON.stringify(playerData));
                    updateTownUI(playerData);
                }, 3000);
            }
        } catch (error) { alert(`שגיאה בקרב: ${error.message}`); }
    });

    document.getElementById('logoutBtn').addEventListener('click', () => { localStorage.removeItem('playerData'); window.location.href = '/index.html'; });
    updateTownUI(playerData);
});
