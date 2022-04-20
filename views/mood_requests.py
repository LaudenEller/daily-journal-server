import sqlite3
from models import Mood
import json

def get_all_moods():
    """ This method will fetch all moods
    """
    
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          SELECT
                            m.id,
                            m.label
                        FROM Moods m
                        """)
        
        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
        return json.dumps(moods)