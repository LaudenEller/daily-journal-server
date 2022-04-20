import sqlite3
from models import Tag
import json

def get_all_tags():
    """ This method will fetch all tags
    """
    
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          SELECT
                            t.id,
                            t.name
                        FROM Tag t
                        """)
        
        tags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            tag = Tag(row['id'], row['name'])
            tags.append(tag.__dict__)
        return json.dumps(tags)