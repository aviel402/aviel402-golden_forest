from flask import Flask, request, jsonify # נשתמש ב-jsonify כדי להחזיר תשובות מסודרות
import os
import psycopg2 # זוהי הספרייה הסטנדרטית בפייתון לחיבור ל-Postgres
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    """פותח חיבור חדש למסד הנתונים"""
    conn = psycopg2.connect(os.environ.get("POSTGRES_URL"))
    return conn

@app.route('/api/register', methods=['POST'])
def register_player():
    """
    זו הפונקציה שתטפל בהרשמה של שחקן חדש.
    היא מצפה לקבל מייל וסיסמה.
    """
    try:
        # קבלת המידע שנשלח מהשחקן
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # בדיקה בסיסית שהמידע הגיע
        if not email or not password:
            return jsonify({'error': 'מייל וסיסמה הם שדות חובה'}), 400

        # מתחברים למסד הנתונים
        conn = get_db_connection()
        cur = conn.cursor()

        # יוצרים טבלה לשחקנים (אם היא עדיין לא קיימת)
        # זה קוד ראשוני, בעתיד נפריד את זה
        cur.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                gold INTEGER DEFAULT 0,
                health INTEGER DEFAULT 100,
                attack INTEGER DEFAULT 10,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        
        # הכנסת השחקן החדש למסד הנתונים
        # בעתיד נוסיף פה הצפנה לסיסמה!
        cur.execute(
            "INSERT INTO players (email, password_hash) VALUES (%s, %s) RETURNING id",
            (email, password)
        )
        player_id = cur.fetchone()[0]

        # שמירת השינויים וסגירת החיבור
        conn.commit()
        cur.close()
        conn.close()

        # החזרת תשובת הצלחה
        return jsonify({
            'message': 'השחקן נוצר בהצלחה!',
            'player_id': player_id
        }), 201

    except psycopg2.IntegrityError:
        # שגיאה שקורית אם המייל כבר קיים במערכת
        return jsonify({'error': 'שחקן עם המייל הזה כבר קיים'}), 409
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'אירעה שגיאה בשרת'}), 500