# קובץ: api/index.py

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

app = Flask(__name__)

# הנתיב לקובץ. /tmp/ הוא המקום היחיד ש-Vercel מרשה לכתוב בו קבצים.
DB_FILE_PATH = '/tmp/players_data.json'

# פונקציית עזר לקריאת הקובץ
def read_players_from_file():
    if not os.path.exists(DB_FILE_PATH):
        return {} # אם הקובץ לא קיים, נחזיר "מסד נתונים" ריק
    try:
        with open(DB_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {} # אם הקובץ ריק או פגום, נתחיל מחדש

# פונקציית עזר לכתיבת הקובץ
def write_players_to_file(data):
    with open(DB_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify(error='יש למלא שם משתמש וסיסמה'), 400

        players = read_players_from_file()

        if username in players:
            return jsonify(error='שם המשתמש הזה כבר תפוס, נסה שם אחר'), 409
        
        players[username] = { 'password_hash': generate_password_hash(password) }
        
        write_players_to_file(players)
        return jsonify(message='השחקן נוצר בהצלחה!'), 201

    except Exception as e:
        return jsonify(error=f"שגיאת שרת בהרשמה: {e}"), 500

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify(error='יש למלא שם משתמש וסיסמה'), 400

        players = read_players_from_file()
        player_data = players.get(username)

        if player_data and check_password_hash(player_data['password_hash'], password):
            player_info_to_return = {'username': username} # אפשר להוסיף פה נתונים מהקובץ אם נרצה
            return jsonify(message='התחברת בהצלחה!', player_data=player_info_to_return), 200
        else:
            return jsonify(error='שם המשתמש או הסיסמה שגויים'), 401
    except Exception as e:
        return jsonify(error=f"שגיאת שרת בכניסה: {e}"), 500
