# קובץ: api/index.py (מעודכן)
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json, os, random # הוספנו את random

app = Flask(__name__)
DB_FILE_PATH = '/tmp/players_data.json'

def read_db(): # ... (נשאר אותו דבר)
def write_db(data): # ... (נשאר אותו דבר)

# (הפונקציות register ו-login נשארות בדיוק אותו דבר)
@app.route('/api/register', methods=['POST'])
def register():
    # ...
    pass
@app.route('/api/login', methods=['POST'])
def login():
    # ...
    pass
    
# ==================
#    נתוני דמות
# ==================
# (גם פונקציה זו נשארת כפי שהייתה)
@app.route('/api/character-data', methods=['GET'])
def get_character_data():
    # ...
    pass

# =======================================================
#               החלק החדש: יציאה להרפתקה
# =======================================================

# "ספר החיות" הראשון שלנו. בעתיד ניקח את זה מרשימת החיות המלאה שלך.
CREATURE_TEMPLATES = {
    'level_1': [
        {'name': 'עכבר שדה', 'health': 20, 'attack': 5, 'gold': 3, 'xp': 10},
        {'name': 'עכביש יער', 'health': 25, 'attack': 7, 'gold': 5, 'xp': 12},
    ]
}

@app.route('/api/adventure/start', methods=['POST'])
def start_adventure():
    try:
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify(error='נדרש שם משתמש כדי לצאת להרפתקה'), 401
            
        # "מגרילים" חיה מהרשימה
        monster_data = random.choice(CREATURE_TEMPLATES['level_1'])
        
        # כדי שהמשחק יזכור מול מי השחקן נלחם,
        # אנחנו צריכים לשמור את זה בקובץ הנתונים שלו
        players = read_db()
        if username in players:
            # מוסיפים "מצב קרב" לשחקן
            players[username]['in_combat_with'] = monster_data
            write_db(players)

            # מחזירים לדפדפן את פרטי המפלצת שהוא פגש
            return jsonify(
                message=f'בשיטוט ביער, נתקלת ב: {monster_data["name"]}!',
                monster=monster_data
            ), 200
        else:
            return jsonify(error='שחקן לא נמצא'), 404

    except Exception as e:
        return jsonify(error=f"שגיאת שרת בהתחלת הרפתקה: {e}"), 500
        # =======================================================
#               החלק החדש: ניהול פעולת קרב
# =======================================================

@app.route('/api/combat/action', methods=['POST'])
def combat_action():
    try:
        data = request.get_json()
        username = data.get('username')
        action = data.get('action') # הפעולה שהשחקן בחר (כרגע רק "attack")

        if not username or not action:
            return jsonify(error='נדרשים שם משתמש ופעולה'), 400

        players = read_db()
        if username not in players:
            return jsonify(error='שחקן לא נמצא'), 404
            
        player_data = players[username]
        monster_data = player_data.get('in_combat_with')
        
        if not monster_data:
             return jsonify(error='השחקן אינו נמצא בקרב כרגע'), 400

        combat_log = [] # נאסוף כאן את כל מה שקרה בתור

        # --- שלב א': השחקן פועל ---
        if action == 'attack':
            # הנחתת נזק על המפלצת
            damage_dealt = player_data.get('attack', 10) # נשתמש בכוח ההתקפה של השחקן בעתיד
            monster_data['health'] -= damage_dealt
            combat_log.append(f"הנחתת מכה אדירה! גרמת {damage_dealt} נזק ל{monster_data['name']}.")
            
            # בדיקה אם המפלצת הובסה
            if monster_data['health'] <= 0:
                xp_gain = monster_data.get('xp', 0)
                gold_gain = monster_data.get('gold', 0)
                
                player_data['xp'] += xp_gain
                player_data['gold'] += gold_gain
                player_data['in_combat_with'] = None # הקרב הסתיים
                write_db(players)
                
                combat_log.append(f"הבסת את ה{monster_data['name']}! קיבלת {xp_gain} ניסיון ו-{gold_gain} זהב.")
                return jsonify(combat_over=True, log=combat_log, player_data=player_data)

        # --- שלב ב': המפלצת פועלת (אם היא עדיין חיה) ---
        damage_taken = monster_data.get('attack', 5)
        player_data['health'] -= damage_taken # נשמור את חיים השחקן בעתיד
        combat_log.append(f"ה{monster_data['name']} משיב מלחמה! ספגת {damage_taken} נזק.")

        # בדיקה אם השחקן הובס
        if player_data['health'] <= 0:
            player_data['in_combat_with'] = None # הקרב הסתיים
            # כאן בעתיד נוסיף לוגיקה של "מוות"
            write_db(players)
            combat_log.append("הובסת בקרב!")
            return jsonify(combat_over=True, log=combat_log, player_data=player_data)
            
        # --- שלב ג': שמירת המצב המעודכן ---
        players[username] = player_data
        write_db(players)

        # מחזירים את כל המידע המעודכן לדפדפן
        return jsonify(
            combat_over=False, 
            log=combat_log, 
            player_data=player_data,
            monster_data=monster_data
        )

    except Exception as e:
        return jsonify(error=f"שגיאת שרת בקרב: {e}"), 500