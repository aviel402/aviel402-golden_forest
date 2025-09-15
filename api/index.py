# קובץ: api/index.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import random

app = Flask(__name__)
DB_FILE_PATH = '/tmp/players_data.json'

def read_players_db():
    if not os.path.exists(DB_FILE_PATH): return {}
    try:
        with open(DB_FILE_PATH, 'r') as f: return json.load(f)
    except: return {}

def write_players_db(data):
    with open(DB_FILE_PATH, 'w') as f: json.dump(data, f, indent=4)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password: return jsonify(error='יש למלא שם משתמש וסיסמה'), 400
        
        players = read_players_db()
        if username in players: return jsonify(error='שם המשתמש הזה כבר תפוס'), 409
        
        players[username] = {'password_hash': generate_password_hash(password),'level': 1,'xp': 0,'gold': 0,'health': 100,'attack': 10}
        write_players_db(players)
        return jsonify(message='השחקן נוצר בהצלחה!'), 201
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        if not username or not password: return jsonify(error='יש למלא שם משתמש וסיסמה'), 400
        
        players = read_players_db()
        player_data = players.get(username)
        if player_data and check_password_hash(player_data['password_hash'], password):
            player_info = {'username': username,'level': player_data.get('level', 1),'xp': player_data.get('xp', 0),'gold': player_data.get('gold', 0),'health': player_data.get('health', 100),'attack': player_data.get('attack', 10)}
            return jsonify(message='התחברת בהצלחה!', player_data=player_info), 200
        else:
            return jsonify(error='שם המשתמש או הסיסמה שגויים'), 401
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

CREATURE_TEMPLATES = [{'name': 'עכבר שדה', 'health': 20, 'attack': 5, 'gold': 3, 'xp': 10},{'name': 'עכביש יער', 'health': 25, 'attack': 7, 'gold': 5, 'xp': 12}]

@app.route('/api/adventure/start', methods=['POST'])
def start_adventure():
    try:
        data = request.get_json()
        username = data.get('username')
        if not username: return jsonify(error='שחקן לא ידוע'), 401
        
        players = read_players_db()
        if username in players:
            monster_data = random.choice(CREATURE_TEMPLATES)
            players[username]['in_combat_with'] = monster_data
            write_players_db(players)
            return jsonify(message=f'בשיטוט ביער, נתקלת ב: {monster_data["name"]}!', monster=monster_data), 200
        return jsonify(error='שחקן לא נמצא'), 404
    except Exception as e: return jsonify(error=f"שגיאת שרת: {e}"), 500

@app.route('/api/combat/action', methods=['POST'])
def combat_action():
    try:
        data = request.get_json(); username, action = data.get('username'), data.get('action')
        if not username or not action: return jsonify(error='חסרים נתונים'), 400
        
        players = read_players_db(); player_data = players.get(username)
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
                write_players_db(players)
                return jsonify(combat_over=True, log=log, player_data=player_data)
        
        damage_taken = monster_data.get('attack', 5)
        player_data['health'] -= damage_taken
        log.append(f"ספגת {damage_taken} נזק.")
        
        if player_data['health'] <= 0:
            player_data['health'] = 0 # שלא יהיו חיים במינוס
            player_data['in_combat_with'] = None; log.append("הובסת בקרב!")
            write_players_db(players)
            return jsonify(combat_over=True, log=log, player_data=player_data)
        
        players[username] = player_data
        write_players_db(players)
        return jsonify(combat_over=False, log=log, player_data=player_data, monster_data=monster_data)

    except Exception as e: return jsonify(error=f"שגיאת שרת בקרב: {e}"), 500
