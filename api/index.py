# קובץ: api/index.py
# הגרסה המלאה, המתוקנת והיציבה

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import random

app = Flask(__name__)
DB_FILE_PATH = '/tmp/players_data.json'

# --- פונקציות עזר לקבצים ---
def read_db():
    if not os.path.exists(DB_FILE_PATH): return {}
    try:
        with open(DB_FILE_PATH, 'r', encoding='utf-8') as f: return json.load(f)
    except: return {}
def write_db(data):
    with open(DB_FILE_PATH, 'w', encoding='utf-8') as f: json.dump(data, f, indent=4, ensure_ascii=False)

# --- הגדרת החיות במשחק ---
CREATURE_TEMPLATES = [
    {'name': 'עכבר שדה', 'health': 20, 'attack': 5, 'gold': 3, 'xp': 10},
    {'name': 'עכביש יער', 'health': 25, 'attack': 7, 'gold': 5, 'xp': 12}
]

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username, password = data.get('username'), data.get('password')
        if not username or not password: return jsonify(error='יש למלא שם משתמש וסיסמה'), 400
        
        db = read_db()
        if username in db: return jsonify(error='שם המשתמש הזה כבר תפוס'), 409
        
        # תיקון חשוב: שומרים את כל נתוני ההתחלה של השחקן
        db[username] = {
            'password_hash': generate_password_hash(password),
            'level': 1, 'xp': 0, 'gold': 0, 'health': 100, 'attack': 10
        }
        write_db(db)
        return jsonify(message='השחקן נוצר בהצלחה!'), 201
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username, password = data.get('username'), data.get('password')
        if not username or not password: return jsonify(error='יש למלא שם משתמש וסיסמה'), 400

        db = read_db()
        player_data = db.get(username)

        if player_data and check_password_hash(player_data.get('password_hash'), password):
            # שיפור: מסירים את הסיסמה ומחזירים את כל שאר הנתונים
            del player_data['password_hash']
            player_data['username'] = username
            return jsonify(message='התחברת בהצלחה!', player_data=player_data), 200
        else:
            return jsonify(error='שם המשתמש או הסיסמה שגויים'), 401
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

# =========================
#  התחלת הרפתקה
# =========================
@app.route('/api/adventure/start', methods=['POST'])
def start_adventure():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username: return jsonify(error='שחקן לא ידוע'), 401
        
        db = read_db()
        if username in db:
            monster_data = random.choice(CREATURE_TEMPLATES).copy() # חשוב להעתיק כדי לא לשנות את המקור
            db[username]['in_combat_with'] = monster_data
            write_db(db)
            return jsonify(message=f'בשיטוט ביער, נתקלת ב: {monster_data["name"]}!', monster=monster_data), 200
        return jsonify(error='שחקן לא נמצא'), 404
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

# =========================
#   פעולת קרב
# =========================
@app.route('/api/combat/action', methods=['POST'])
def combat_action():
    try:
        data = request.get_json(); username, action = data.get('username'), data.get('action')
        if not username or not action: return jsonify(error='חסרים נתונים'), 400
        
        db = read_db(); player_data = db.get(username)
        if not player_data: return jsonify(error='שחקן לא נמצא'), 404
            
        monster_data = player_data.get('in_combat_with')
        if not monster_data: return jsonify(error='השחקן אינו בקרב'), 400
        
        log = []
        if action == 'attack':
            damage_dealt = player_data.get('attack', 10)
            monster_data['health'] -= damage_dealt
            log.append(f"גרמת {damage_dealt} נזק ל{monster_data['name']}.")
            
            if monster_data['health'] <= 0:
                xp, gold = monster_data.get('xp',0), monster_data.get('gold',0)
                player_data['xp'] += xp; player_data['gold'] += gold
                player_data['in_combat_with'] = None
                log.append(f"הבסת את {monster_data['name']}! קיבלת {xp} ניסיון ו-{gold} זהב.")
                write_db(db)
                # מחזירים את נתוני השחקן המעודכנים
                del player_data['password_hash']
                player_data['username'] = username
                return jsonify(combat_over=True, log=log, player_data=player_data)
        
        damage_taken = monster_data.get('attack', 5)
        player_data['health'] -= damage_taken
        log.append(f"ספגת {damage_taken} נזק.")
        
        if player_data['health'] <= 0:
            player_data['health'] = 0
            player_data['in_combat_with'] = None
            log.append("הובסת בקרב!")
            write_db(db)
            del player_data['password_hash']
            player_data['username'] = username
            return jsonify(combat_over=True, log=log, player_data=player_data)
        
        db[username] = player_data
        write_db(db)
        
        # נחזיר את נתוני השחקן המעודכנים גם באמצע קרב
        del player_data['password_hash']
        player_data['username'] = username
        return jsonify(combat_over=False, log=log, player_data=player_data, monster_data=monster_data)

    except Exception as e: return jsonify(error=f"שגיאת שרת בקרב: {e}"), 500
