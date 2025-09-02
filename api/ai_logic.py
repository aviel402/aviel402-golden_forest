import random

def decide_monster_action(player, monster):
    """
    זוהי פונקציית ה"מוח" של החיה.
    היא מקבלת את נתוני השחקן והמפלצת, ומחזירה את הפעולה שהוחלט עליה.
    """
    
    # מחשבים את אחוז החיים שנשארו לחיה
    monster_health_percentage = (monster['health'] / monster['max_health']) * 100
    player_health_percentage = (player['health'] / player['max_health']) * 100
    
    # --- כאן מתחיל עץ ההחלטות ---
    
    # 1. מצב ייאוש: החיה פצועה קשה מאוד
    if monster_health_percentage <= 20:
        # יש סיכוי של 50% שהיא תנסה להתרפא, אם לא - תתקוף רגיל
        if random.random() < 0.5:
            return {'action': 'heal', 'power': random.randint(10, 20), 'text': 'החיה נראית מותשת ומנסה לרכז אנרגיה לריפוי!'}
        else:
            return {'action': 'attack_normal', 'power': monster['attack'], 'text': 'בייאושה, החיה תוקפת בפראות!'}

    # 2. הזדמנות: השחקן חלש!
    elif player_health_percentage <= 30:
        # סיכוי גבוה (70%) להשתמש במתקפה חזקה כדי לסיים את הקרב
        if random.random() < 0.7:
             return {'action': 'attack_strong', 'power': int(monster['attack'] * 1.5), 'text': 'החיה מזהה חולשה ותוקפת במלוא העוצמה!'}
        else:
             return {'action': 'attack_normal', 'power': monster['attack'], 'text': 'החיה תוקפת במהירות!'}
             
    # 3. מצב רגיל: הקרב באיזון
    else:
        rand = random.random()
        if rand < 0.65: # 65% סיכוי להתקפה רגילה
            return {'action': 'attack_normal', 'power': monster['attack'], 'text': 'החיה תוקפת!'}
        elif rand < 0.85: # 20% סיכוי להתגונן
            return {'action': 'defend', 'power': 0.5, 'text': 'החיה מתכוננת למכה ומתגוננת!'}
        else: # 15% סיכוי להתקפה חזקה
             return {'action': 'attack_strong', 'power': int(monster['attack'] * 1.5), 'text': 'החיה צוברת כוח למתקפה אדירה!'}
