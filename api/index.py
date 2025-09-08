from flask import Flask, request, jsonify
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
        # שיניתי email ל-username כדי שיתאים לבקשה שלך
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        ''')
        conn.commit()
    except Exception as e:
        print(f"DB Init Warning: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    conn, cur = None, None
    try:
        data = request.get_json(silent=True)
        if not data: return jsonify(error="בקשה לא תקינה"), 400
        username, password = data.get('username'), data.get('password')

        if not username or not password: return jsonify(error="נא למלא שם משתמש וסיסמה"), 400
            
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        if cur.fetchone(): return jsonify(error="שם המשתמש הזה כבר תפוס"), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()

        return jsonify(message="נרשמת בהצלחה! כעת ניתן להתחבר."), 201

    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify(error="אירעה שגיאת שרת פנימית בהרשמה"), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    conn, cur = None, None
    try:
        data = request.get_json(silent=True)
        if not data: return jsonify(error="בקשה לא תקינה"), 400
        username, password = data.get('username'), data.get('password')

        if not username or not password: return jsonify(error="נא למלא שם משתמש וסיסמה"), 400

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, password_hash FROM players WHERE username = %s", (username,))
        player = cur.fetchone()

        if player and check_password_hash(player['password_hash'], password):
            player_data = {'id': player['id'], 'username': username}
            return jsonify(message="התחברת בהצלחה!", player_data=player_data), 200
        else:
            return jsonify(error="שם המשתמש או הסיסמה שגויים"), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify(error="אירעה שגיאת שרת פנימית בכניסה"), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()
