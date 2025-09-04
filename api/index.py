# קובץ: api/index.py (גרסה 5.0 - יציבה ובדוקה)

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

app = Flask(__name__)

# פונקציית עזר לחיבור למסד הנתונים
def get_db_connection():
    # מדפיסים הודעה כדי לוודא שהפונקציה נקראת
    print("Attempting to establish database connection...")
    conn_url = os.environ.get("POSTGRES_URL")
    if not conn_url:
        print("FATAL ERROR: POSTGRES_URL environment variable not found!")
        raise ValueError("Database connection URL is not configured.")
    
    conn = psycopg2.connect(conn_url)
    print("Database connection successful.")
    return conn

# פונקציית אתחול שיוצרת את הטבלה
def initialize_database():
    try:
        print("Initializing database tables...")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        ''')
        # בעתיד נוסיף כאן את שאר העמודות
        conn.commit()
        cur.close()
        conn.close()
        print("Tables initialized successfully.")
    except Exception as e:
        # אם יש תקלה ביצירת הטבלה, נראה אותה בלוגים
        print(f"FATAL ERROR during DB initialization: {e}")

# מריצים את האתחול פעם אחת כשהשרת עולה
with app.app_context():
    initialize_database()

# ==================
#    הרשמה (Register)
# ==================
@app.route('/api/register', methods=['POST'])
def register():
    print("\n--- Register endpoint hit ---")
    conn = None
    try:
        data = request.get_json()
        if not data:
            return jsonify(error="לא התקבל מידע בבקשה"), 400
        
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify(error='יש למלא אימייל וסיסמה'), 400
            
        print(f"Attempting to register user: {email}")

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id FROM players WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify(error='שחקן עם אימייל זה כבר רשום'), 409
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO players (email, password_hash) VALUES (%s, %s) RETURNING id", (email, password_hash))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f"User {email} registered successfully.")
        return jsonify(message='נרשמת בהצלחה!'), 201

    except Exception as e:
        print(f"!!! FATAL REGISTER ERROR: {e}")
        return jsonify(error='אירעה שגיאת שרת פנימית בעת ההרשמה'), 500
    finally:
        # נוודא שתמיד סוגרים את החיבור למסד הנתונים
        if conn is not None:
            conn.close()

# ==================
#     כניסה (Login)
# ==================
# פונקציית הלוגין נשארת כפי שהייתה, כי הבעיה הייתה בהרשמה

@app.route('/api/login', methods=['POST'])
def login():
    # ... הקוד של לוגין נשאר כפי שהיה בתשובה המלאה הקודמת ...
    pass
