# קובץ: api/db_utils.py
import psycopg2
import os

def get_db_connection():
    """פונקציה מרכזית שפותחת חיבור למסד הנתונים"""
    conn_url = os.environ.get("POSTGRES_URL")
    if not conn_url:
        raise Exception("לא הוגדרה כתובת למסד הנתונים")
    conn = psycopg2.connect(conn_url)
    return conn

def init_db():
    """פונקציה שיוצרת את טבלאות הבסיס בפעם הראשונה שנריץ אותה"""
    conn = get_db_connection()
    cur = conn.cursor()
    # יצירת טבלת משתמשים
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    # יצירת טבלת דמויות (מקושרת למשתמש)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id SERIAL PRIMARY KEY,
            user_id INTEGER UNIQUE NOT NULL REFERENCES users(id),
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 0,
            health INTEGER DEFAULT 100,
            max_health INTEGER DEFAULT 100,
            attack INTEGER DEFAULT 10,
            defense INTEGER DEFAULT 5,
            speed INTEGER DEFAULT 5,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()