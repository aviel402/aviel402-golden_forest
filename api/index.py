# קובץ: api/index.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

app = Flask(__name__)
DB_FILE_PATH = '/tmp/players_db.json'

def read_db():
    if not os.path.exists(DB_FILE_PATH): return {}
    try:
        with open(DB_FILE_PATH, 'r') as f: return json.load(f)
    except: return {}

def write_db(data):
    with open(DB_FILE_PATH, 'w') as f: json.dump(data, f, indent=4)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username, password = data.get('username'), data.get('password')
        if not username or not password: return jsonify(error='נא למלא שם משתמש וסיסמה'), 400
        db = read_db()
        if username in db: return jsonify(error='שם המשתמש תפוס'), 409
        db[username] = {
            'password_hash': generate_password_hash(password),
            'level': 1, 'xp': 0, 'gold': 0
        }
        write_db(db)
        return jsonify(message='השחקן נוצר בהצלחה!'), 201
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username, password = data.get('username'), data.get('password')
        if not username or not password: return jsonify(error='נא למלא שם משתמש וסיסמה'), 400
        db = read_db()
        player_data = db.get(username)
        if player_data and check_password_hash(player_data['password_hash'], password):
            player_info = {'username': username, 'level': player_data.get('level',1), 'xp': player_data.get('xp',0), 'gold': player_data.get('gold',0)}
            return jsonify(message='התחברת בהצלחה!', player_data=player_info), 200
        else:
            return jsonify(error='שם המשתמש או הסיסמה שגויים'), 401
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500