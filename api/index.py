# קובץ: api/index.py
# מכיל את כל הלוגיקה של השרת

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras 
import os

app = Flask(__name__)

# פונקציית עזר לחיבור למסד הנתונים
def get_db_connection():
    conn_url = os.environ.get("POSTGRES_URL")
    conn = psycopg2.connect(conn_url)
    return conn

# יצירת טבלאות
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

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register_player():
    try:
        data = request.json
        email, password = data.get('email'), data.get('password')
        if not email or not password: return jsonify(error='מייל וסיסמה חובה'), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM players WHERE email = %s", (email,))
        if cur.fetchone(): return jsonify(error='שחקן עם מייל זה כבר קיים'), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (email, password_hash) VALUES (%s, %s) RETURNING id", (email, password_hash))
        player_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message='השחקן נוצר בהצלחה!', player_id=player_id), 201
    except Exception as e:
        return jsonify(error='שגיאת שרת בהרשמה'), 500

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login_player():
    try:
        data = request.json
        email, password = data.get('email'), data.get('password')
        if not email or not password: return jsonify(error='מייל וסיסמה חובה'), 400

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
        cur.execute("SELECT id, password_hash FROM players WHERE email = %s", (email,))
        player = cur.fetchone()
        cur.close()
        conn.close()
        
        if player and check_password_hash(player['password_hash'], password):
            return jsonify(message='התחברת בהצלחה!', player_id=player['id']), 200
        else:
            return jsonify(error='פרטי ההתחברות שגויים'), 401
    except Exception as e:
        return jsonify(error='שגיאת שרת בכניסה'), 500

# ==================
#    נתוני דמות
# ==================
@app.route('/api/character-data', methods=['GET'])
def get_character_data():
    player_id = request.args.get('player_id')
    if not player_id: return jsonify(error='נדרש מזהה שחקן'), 401
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT email, level, xp, gold FROM players WHERE id = %s", (player_id,))
        player_data = cur.fetchone()
        cur.close()
        conn.close()
        
        if not player_data: return jsonify(error='שחקן לא נמצא'), 404
        return jsonify(player_data), 200
    except Exception as e:
        return jsonify(error='שגיאת שרת בטעינת נתונים'), 500