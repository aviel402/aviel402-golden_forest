# קובץ: api/index.py

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)

# הנתיב לקובץ שבו נשמור את המידע. /tmp/ הוא המקום היחיד ש-Vercel מרשה לכתוב אליו.
PLAYERS_DB_FILE = '/tmp/players_db.json'

# פונקציית עזר לקריאת הקובץ
def read_db():
    if not os.path.exists(PLAYERS_DB_FILE):
        return {}
    with open(PLAYERS_DB_FILE, 'r') as f:
        # try-except למקרה שהקובץ ריק או פגום
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# פונקציית עזר לכתיבת הקובץ
def write_db(data):
    with open(PLAYERS_DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        # שינוי: עובדים עם שם משתמש במקום אימייל
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify(error='יש למלא שם משתמש וסיסמה'), 400

        db = read_db()
        if username in db:
            return jsonify(error='שם המשתמש הזה כבר תפוס'), 409
        
        db[username] = {
            'password_hash': generate_password_hash(password),
            'level': 1,
            'xp': 0,
            'gold': 0
        }
        
        write_db(db)
        return jsonify(message='השחקן נוצר בהצלחה!'), 201

    except Exception as e:
        return jsonify(error=f"שגיאת שרת בהרשמה: {e}"), 500

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify(error='יש למלא שם משתמש וסיסמה'), 400

        db = read_db()
        player_data = db.get(username)

        if player_data and check_password_hash(player_data['password_hash'], password):
            # מחזירים את כל הנתונים של השחקן, חוץ מהסיסמה המוצפנת
            player_info_to_return = {
                'username': username,
                'level': player_data.get('level', 1),
                'xp': player_data.get('xp', 0),
                'gold': player_data.get('gold', 0)
            }
            return jsonify(message='התחברת בהצלחה!', player_data=player_info_to_return), 200
        else:
            return jsonify(error='שם המשתמש או הסיסמה שגויים'), 401
    except Exception as e:
        return jsonify(error=f"שגיאת שרת בכניסה: {e}"), 500
