# קובץ: index.py

from flask import Flask

app = Flask(__name__)

# זו הפונקציה הראשית שתטפל בכל הבקשות
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # נחזיר דף HTML פשוט עם JavaScript מוטמע בתוכו
    # זו הדרך הכי בטוחה לוודא שהכל נטען ביחד
    
    html_content = """
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>בדיקה</title>
    </head>
    <body>
        <h1>אם אתה רואה את זה, שרת הפייתון עובד.</h1>
        <button id="testButton">לחץ כאן לבדיקה</button>
        <p id="message"></p>
        
        <script>
            // קוד JavaScript פשוט וברור, מוטמע ישירות
            console.log("JavaScript נטען!");

            document.addEventListener('DOMContentLoaded', function() {
                const button = document.getElementById('testButton');
                const message = document.getElementById('message');

                if (button) {
                    button.addEventListener('click', function() {
                        message.textContent = "הצלחה! הלחיצה עבדה!";
                        message.style.color = 'green';
                        alert('הכפתור נלחץ והגיב!');
                    });
                }
            });
        </script>
        
    </body>
    </html>
    """
    return html_content, 200, {'Content-Type': 'text/html; charset=utf-8'}
