# קובץ: api/game.py
from flask import Blueprint, request, jsonify
from db_utils import get_db_connection
game_bp = Blueprint('game_bp', __name__)

@game_bp.route('/town', methods=['GET'])
def town():
    # כאן נחזיר את המצב הנוכחי של השחקן (חיים, זהב, וכו')
    return jsonify({"message": "העיירה - בפיתוח"})

@game_bp.route('/adventure', methods=['POST'])
def start_adventure():
    # כאן נתחיל הרפתקה, ניצור מפגש אקראי עם חיה
    return jsonify({"message": "הרפתקה - בפיתוח"})

@game_bp.route('/combat', methods=['POST'])
def combat_action():
    # כאן תהיה לוגיקת הקרב - התקפה, הגנה וכו'
    return jsonify({"message": "קרב - בפיתוח"})