# קובץ: api/index.py

from flask import Flask, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras 
import os

app = Flask(__name__)

# פונקציית עזר לחיבור למסד הנתונים
def get_db_connection():
    conn_url = os.environ.get("POSTGRES_URL")
    if not conn_url:
        raise Exception("לא הוגדרה כתובת למסד הנתונים POSTGRES_URL")
    conn = psycopg2.connect(conn_url)
    return conn

# יצירת הטבלה הראשונית אם אינה קיימת
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT-NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            level INTEGER DEFAULT 1, 
            xp INTEGER DEFAULT 0, 
            gold INTEGER DEFAULT 0
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

# קריאה לפונקציית אתחול הדאטהבייס בפעם הראשונה שהשרת עולה
# שימוש ב-app.app_context() מבטיח שזה יקרה בהקשר הנכון
with app.app_context():
    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
     return jsonify(message="שרת 'יער הזהב' פעיל"), 200

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

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM players WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify(error='שחקן עם המייל הזה כבר קיים'), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (email, password_hash) VALUES (%s, %s) RETURNING id", (email, password_hash))
        player_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message='השחקן נוצר בהצלחה! כעת תוכל להתחבר.', player_id=player_id), 201

    except Exception as e:
        print(f"Register Error: {e}")
        return jsonify(error='אירעה שגיאה בשרת בעת ההרשמה'), 500

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

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) 
        
        cur.execute("SELECT id, password_hash FROM players WHERE email = %s", (email,))
        player = cur.fetchone()

        if player is None or not check_password_hash(player['password_hash'], password):
            return jsonify(error='המייל או הסיסמה שהוזנו אינם נכונים'), 401
        
        cur.close()
        conn.close()
        
        return jsonify(message='התחברת בהצלחה!', player_id=player['id']), 200

    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify(error='אירעה שגיאה בשרת בעת ניסיון ההתחברות'), 500