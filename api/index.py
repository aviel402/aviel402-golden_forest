# קובץ: api/index.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras 
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(os.environ.get("POSTGRES_URL"))

with app.app_context():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                level INTEGER DEFAULT 1, xp INTEGER DEFAULT 0, gold INTEGER DEFAULT 0
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Init Error: {e}")

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data, email, password = request.get_json(), data.get('email'), data.get('password')
        if not email or not password: return jsonify(error="יש למלא אימייל וסיסמה"), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM players WHERE email = %s", (email,))
        if cur.fetchone(): return jsonify(error="שחקן עם אימייל זה כבר רשום"), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (email, password_hash) VALUES (%s, %s) RETURNING id", (email, password_hash))
        player_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message="נרשמת בהצלחה! כעת ניתן להתחבר."), 201

    except Exception as e:
        return jsonify(error=f"שגיאת שרת בהרשמה"), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email, password = data.get('email'), data.get('password')
        if not email or not password: return jsonify(error="יש למלא אימייל וסיסמה"), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM players WHERE email = %s", (email,))
        player = cur.fetchone()
        
        if player and check_password_hash(player['password_hash'], password):
            # === התיקון הקריטי: מחזירים אובייקט player_data ולא רק player_id ===
            player_info_to_return = {
                'id': player['id'],
                'email': player['email'],
                'level': player['level'],
                'xp': player['xp'],
                'gold': player['gold']
            }
            cur.close()
            conn.close()
            return jsonify(message="התחברת בהצלחה!", player_data=player_info_to_return), 200
        else:
            cur.close()
            conn.close()
            return jsonify(error="האימייל או הסיסמה שגויים"), 401
    except Exception as e:
        return jsonify(error=f"שגיאת שרת בכניסה"), 500
