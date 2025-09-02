# קובץ: api/index.py (גרסה שעובדת עם קבצי JSON)

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)

# הגדרת הנתיב לקובץ הנתונים. חשוב: /tmp/ הוא המקום היחיד שבו Vercel מאפשרת כתיבה
DB_FILE_PATH = '/tmp/players.json'

# פונקציית עזר לקריאת נתוני השחקנים מהקובץ
def read_players_db():
    if not os.path.exists(DB_FILE_PATH):
        return {} # אם הקובץ לא קיים, נחזיר מילון ריק
    with open(DB_FILE_PATH, 'r') as f:
        return json.load(f)

# פונקציית עזר לכתיבת נתוני השחקנים לקובץ
def write_players_db(data):
    with open(DB_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register_player():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify(error='מייל וסיסמה הם שדות חובה'), 400

        players = read_players_db()

        if email in players:
            return jsonify(error='שחקן עם המייל הזה כבר קיים'), 409
        
        password_hash = generate_password_hash(password)
        
        # הוספת השחקן החדש למילון
        players[email] = {
            'password_hash': password_hash,
            'level': 1,
            'xp': 0,
            'gold': 0
        }
        
        write_players_db(players)
        
        return jsonify(message='השחקן נוצר בהצלחה!'), 201

    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify(error='אירעה שגיאה בשרת'), 500

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login_player():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify(error='מייל וסיסמה הם שדות חובה'), 400

        players = read_players_db()
        player_data = players.get(email)

        if player_data is None or not check_password_hash(player_data['password_hash'], password):
            return jsonify(error='המייל או הסיסמה שהוזנו אינם נכונים'), 401
        
        # מחזירים את כל נתוני השחקן (בלי הסיסמה)
        return jsonify(
            message='התחברת בהצלחה!',
            player_data={
                'email': email,
                'level': player_data['level'],
                'xp': player_data['xp'],
                'gold': player_data['gold']
            }
        ), 200

    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify(error='אירעה שגיאה בשרת'), 500
