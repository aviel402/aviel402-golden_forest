# קובץ: index.py
from flask import Flask
# מייבאים את החלקים השונים של האפליקציה
from api.auth import auth_bp
from api.game import game_bp
from api.db_utils import init_db

app = Flask(__name__)

# הרשמת ה-"Blueprints" - חיבור החלקים השונים לאפליקציה הראשית
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(game_bp, url_prefix='/api/game')

# פקודה ראשונית להפעלת מסד הנתונים
# בפעם הראשונה שתריץ את זה, זה ייצור את הטבלאות
with app.app_context():
    init_db()

@app.route('/')
def home():
    return "שרת המשחק 'ארץ הפרא' פעיל."