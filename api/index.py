# קובץ: api/index.py (עם ספר חיות מורחב)

from flask import Flask, request, jsonify
# ... שאר הייבואים נשארים אותו דבר

app = Flask(__name__)
DB_FILE_PATH = '/tmp/players_data.json'

def read_db(): # ...
def write_db(data): # ...

# =======================================================
#               "ספר החיות" של יער הזהב
# =======================================================
CREATURE_BOOK = {
    "tier1": [ # חיות שמופיעות ברמות 1-3
        {'name': 'עכבר שדה', 'health': 15, 'attack': 3, 'gold': 2, 'xp': 8, 'sprite_id': 'mouse'},
        {'name': 'יתוש ענק', 'health': 10, 'attack': 4, 'gold': 1, 'xp': 7, 'sprite_id': 'mosquito'},
        {'name': 'צב קטן', 'health': 30, 'attack': 2, 'gold': 4, 'xp': 10, 'sprite_id': 'turtle'}
    ],
    "tier2": [ # חיות שמופיעות ברמות 4-6
        {'name': 'שועל ערמומי', 'health': 40, 'attack': 10, 'gold': 15, 'xp': 25, 'sprite_id': 'fox'},
        {'name': 'נחש צפע', 'health': 35, 'attack': 12, 'gold': 20, 'xp': 30, 'sprite_id': 'snake'},
        {'name': 'חזיר בר', 'health': 60, 'attack': 8, 'gold': 12, 'xp': 28, 'sprite_id': 'boar'}
    ],
    "tier3": [ # חיות שמופיעות ברמות 7+
        {'name': 'זאב בודד', 'health': 80, 'attack': 20, 'gold': 30, 'xp': 50, 'sprite_id': 'wolf'},
        {'name': 'דוב צעיר', 'health': 120, 'attack': 15, 'gold': 40, 'xp': 60, 'sprite_id': 'bear'},
    ]
}

# ==================
#    הרשמה, כניסה (נשארים ללא שינוי)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    # ...
    pass
@app.route('/api/login', methods=['POST'])
def login():
    # ...
    pass
    
# =========================
#  התחלת הרפתקה (הגרסה המשודרגת)
# =========================
@app.route('/api/adventure/start', methods=['POST'])
def start_adventure():
    try:
        username = request.json.get('username')
        db = read_db()
        
        if not username or username not in db: 
            return jsonify(error='שחקן לא נמצא'), 404
        
        player_level = db[username].get('level', 1)
        
        # --- כאן הקסם: בחירת חיה לפי רמת השחקן ---
        available_creatures = []
        if player_level <= 3:
            available_creatures.extend(CREATURE_BOOK['tier1'])
        if player_level >= 2 and player_level <= 6:
            available_creatures.extend(CREATURE_BOOK['tier2'])
        if player_level >= 5:
            available_creatures.extend(CREATURE_BOOK['tier3'])
        
        # אם אין חיות מתאימות (למקרה חירום), ניקח מהרמה הראשונה
        if not available_creatures:
            available_creatures = CREATURE_BOOK['tier1']
            
        monster_data = random.choice(available_creatures).copy()
        db[username]['in_combat_with'] = monster_data
        write_db(db)
        
        return jsonify(message=f'בעומק היער, פגשת {monster_data["name"]}!', monster=monster_data), 200

    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

# =========================
#   פעולת קרב (נשארת ללא שינוי כרגע)
# =========================
@app.route('/api/combat/action', methods=['POST'])
def combat_action():
    # ...
    pass
