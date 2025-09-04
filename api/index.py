# קובץ: api/index.py (גרסה 6.0 - עם תיקון JSON וכל שאר התיקונים)

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2, psycopg2.extras, os

app = Flask(__name__)

# פונקציית עזר לחיבור למסד הנתונים
def get_db():
    conn_url = os.environ.get("POSTGRES_URL")
    if not conn_url: raise Exception(" משתנה הסביבה POSTGRES_URL אינו מוגדר")
    return psycopg2.connect(conn_url)

# יצירת הטבלה אם אינה קיימת, בפעם הראשונה שהשרת עולה
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
    except Exception as e:
        print(f"DB Init Warning: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

# נקודת הקצה הראשית. תפקידה לאשר שהשרת חי.
# חשוב שהיא תחזיר תשובה בפורמט JSON
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
     return jsonify(message="שרת 'יער הזהב' פעיל"), 200

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    conn, cur = None, None
    try:
        data = request.get_json(silent=True)
        if not data: return jsonify(error="בקשה לא תקינה"), 400
        email, password = data.get('email'), data.get('password')

        if not email or not password: return jsonify(error="נא למלא אימייל וסיסמה"), 400
            
        conn = get_db()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM players WHERE email = %s", (email,))
        if cur.fetchone(): return jsonify(error="האימייל הזה כבר רשום במערכת"), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (email, password_hash) VALUES (%s, %s)", (email, password_hash))
        conn.commit()

        return jsonify(message="נרשמת בהצלחה! כעת ניתן להתחבר."), 201

    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify(error="אירעה שגיאת שרת פנימית בעת ההרשמה"), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()

# ==================
#     כניסה (Login)
# ==================
@app.route('/api/login', methods=['POST'])
def login():
    conn, cur = None, None
    try:
        data = request.get_json(silent=True)
        if not data: return jsonify(error="בקשה לא תקינה"), 400
        email, password = data.get('email'), data.get('password')

        if not email or not password: return jsonify(error="נא למלא אימייל וסיסמה"), 400

        conn = get_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT id, password_hash FROM players WHERE email = %s", (email,))
        player = cur.fetchone()

        if player and check_password_hash(player['password_hash'], password):
            return jsonify(message="התחברת בהצלחה!", player_id=player['id']), 200
        else:
            return jsonify(error="האימייל או הסיסמה שגויים"), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify(error="אירעה שגיאת שרת פנימית בעת ההתחברות"), 500
    finally:
        if cur: cur.close()
        if conn: conn.close()
