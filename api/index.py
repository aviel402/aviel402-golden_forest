# קובץ: api/index.py (גרסה יציבה)
from flask import Flask, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2, psycopg2.extras, os

app = Flask(__name__)

def get_db():
    conn = psycopg2.connect(os.environ.get("POSTGRES_URL"))
    return conn

with app.app_context():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
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
        data = request.get_json()
        email, password = data.get('email'), data.get('password')

        if not email or not password: return jsonify(error="יש למלא אימייל וסיסמה"), 400
        
        conn = get_db()
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
        return jsonify(error=f"שגיאת שרת בהרשמה: {e}"), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email, password = data.get('email'), data.get('password')
        if not email or not password: return jsonify(error="יש למלא אימייל וסיסמה"), 400

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, password_hash FROM players WHERE email = %s", (email,))
        player = cur.fetchone()
        cur.close()
        conn.close()

        if player and check_password_hash(player['password_hash'], password):
            return jsonify(message="התחברת בהצלחה!", player_id=player['id']), 200
        else:
            return jsonify(error="האימייל או הסיסמה שגויים"), 401
    except Exception as e:
        return jsonify(error=f"שגיאת שרת בכניסה: {e}"), 500
