# קובץ: api/content_generator.py
# מנוע ליצירת חיות ייחודיות באמצעות Gemini

import google.generativeai as genai
import os
import random

# טוען את מפתח ה-API שהגדרנו ב-Vercel
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest') # המודל הכי חדש וחזק

def create_new_creature():
    """
    פונה ל-Gemini ומבקש ממנו "לברוא" חיה חדשה.
    מחזיר את שם החיה, תיאורה, ואת התמונה שלה.
    """
    try:
        # ההנחיה (prompt) ל-AI. זוהי האומנות האמיתית.
        # אנחנו נותנים לו קצת קונטקסט ומבקשים ממנו להיות יצירתי.
        prompt = """
        אתה אמן ומספר סיפורים בעולם פנטזיה בשם 'יער הזהב'. 
        אני צריך שתיצור עבורי חיה חדשה, מקורית ומעניינת שנמצאת ביער. 
        אני רוצה לקבל ממך שם ייחודי לחיה, ותיאור קצר ומסקרן שלה (בערך 2-3 משפטים).
        בנוסף, תן לי הנחיה (prompt) באנגלית ליצירת תמונה של החיה הזאת, בסגנון ציור שמן דיגיטלי, פנטסטי ומפורט.
        
        החזר לי את התשובה בפורמט JSON הבא בדיוק:
        {
            "name": "שם החיה",
            "description": "תיאור קצר ומסקרן בעברית.",
            "image_prompt": "prompt in English for a digital oil painting"
        }
        """

        response = model.generate_content(prompt)
        # מנקים את התגובה כדי לקבל JSON נקי
        clean_response = response.text.replace('```json', '').replace('```', '').strip()
        
        # טוענים את התשובה לתוך מילון פייתון
        creature_data = json.loads(clean_response)
        
        # --- כאן נוכל להוסיף בעתיד יצירת תמונה אמיתית ---
        # image_response = genai.generate_image(prompt=creature_data['image_prompt'])
        # creature_data['image_url'] = image_response.url
        
        return creature_data
        
    except Exception as e:
        print(f"AI content generation error: {e}")
        # אם יש תקלה, נחזיר חיה ברירת מחדל כדי שהמשחק לא ייתקע
        return {
            "name": "שדון היער",
            "description": "יצור קטן וזריז החי בין שורשי העצים העתיקים.",
            "image_prompt": "a small goblin hiding in the roots of an ancient tree, digital oil painting style"
        }