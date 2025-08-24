# קובץ: api/auth.py
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from db_utils import get_db_connection # נייבא את פונקציית החיבור מקובץ משותף

# חשוב: בפייתון, אנחנו יכולים להשתמש ב-"Blueprint" כדי לפצל את האפליקציה לחלקים
from flask import Blueprint
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # ... כאן תהיה הלוגיקה של ההרשמה (יצירת משתמש ודמות)
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "נדרשים מייל וסיסמה"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    
    # בדיקה אם המשתמש כבר קיים
    cur.execute("SELECT id FROM users WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "משתמש עם מייל זה כבר קיים"}), 409
        
    # הצפנת הסיסמה
    password_hash = generate_password_hash(password)
    
    # יצירת המשתמש החדש
    cur.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id", (email, password_hash))
    user_id = cur.fetchone()[0]
    
    # יצירת דמות (character) חדשה עבור המשתמש
    cur.execute("INSERT INTO characters (user_id) VALUES (%s)", (user_id,))
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "משתמש נוצר בהצלחה"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    # ... כאן תהיה הלוגיקה של הכניסה
    return jsonify({"message": "לוגיקה של כניסה - בפיתוח"})