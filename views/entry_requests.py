import sqlite3
from models import Journal_entries, Mood, Tag
import json

def get_all_entries():
    
    """This method will fetch all entries"""
    
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        
        conn.row_factory = sqlite3.Row
        
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                e.id,
                e.concept,
                e.entry,
                e.moodId,
                e.date,
                m.label,
                t.name tag_name
            FROM journal_entries e
            JOIN Moods m
            ON m.id = e.moodId
                        """)
        
        entries = []

        dataset = db_cursor.fetchall()                # db_cursor has value of Sql query from .execute(), converts results to data form set by line 12
                                                            # .fetchall() sets dataset to iterable python datatype
        # db_cursor.execute("""
        #                 SELECT
        #                     t.name
        #                 FROM Tag t
        #                 JOIN Entrytag et
        #                 ON et.tag_id = t.id
        #                 """)
        
        # entry_tags = db_cursor.fetchall()

        for row in dataset:
            
            tags = []
            # Use method that checks the entries list for the entry ids, if there is an entry dictionary with that entry id, get the new tag and push it to the existing dictionary
                # If there isn't an entry dictionary with that entry id, create a new entry and push it to the list
            # if row['id'] in entries:
            #     tag = Tag(row['t.id'], row['tag_name'])
            #     tags.append(tag)
            # else:
                
            
            #Conditional statement that checks entry ids and if so, gets tag and pushes into existing list of tags. If not, creates new entries for new ids, but pushes tags to existing 
             
            entry = Journal_entries(row['id'], row['concept'], row['entry'], row['moodId'],
                        row['date'], )
        
            mood = Mood(row['id'], row['label'])
            
            db_cursor.execute("""
                            SELECT
                                t.id,
                                t.name tag_name
                            FROM journal_entries e
                            JOIN Entrytag et
                            ON et.entry_id = e.id
                            LEFT JOIN Tag t
                            ON et.tag_id = t.id
                            WHERE et.entry_id = ?
                            """, ( entry.id, ))
            entry_tags = db_cursor.fetchall()

            for et in entry_tags:
                tag = Tag(et['id'], et['tag_name'])
                tags.append(tag)
        
            entry.tags = tags.__dict__

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

        return json.dumps(entries)

def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                e.id,
                e.concept,
                e.entry,
                e.moodId,
                e.date
            FROM journal_entries e
            WHERE e.id = ?
            """, ( id, ))
        
        data = db_cursor.fetchone()
        
        entry = Journal_entries(data['id'], data['concept'], data['entry'],
                                data['moodId'], data['date'])
        
        return json.dumps(entry.__dict__)
    
def get_entries_by_search(string_variable):
    """This method gets entries by mood id"""
    
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            SELECT
                e.id,
                e.concept,
                e.entry,
                e.moodId,
                e.date
            FROM journal_entries e
           WHERE e.entry LIKE ?
            """, ( '%'+ string_variable +'%', ))
        
        entries = []
        
        data = db_cursor.fetchall()
        
        for row in data:
            entry = Journal_entries(row['id'], row['concept'], row['entry'], row['moodId'], row['date'])
            
            entries.append(entry.__dict__)
            
        return json.dumps(entries)
    
def delete_entry(id):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            DELETE FROM journal_entries
            WHERE id = ?
            """, ( id, ))
        
def create_entry(new_entry):
    """This method is responsible for handling POST requests"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            INSERT INTO journal_entries
            (concept, entry, moodId, date)
            VALUES
            (?, ?, ?, ?);
            """, (new_entry['concept'], new_entry['entry'], new_entry['moodId'], new_entry['date']))
        
        id = db_cursor.lastrowid
        
        new_entry['id'] = id
        
        for tag in new_entry['tags']:
            db_cursor.execute("""
                INSERT INTO Entrytag
                ( entry_id, tag_id)
                VALUES
                ( ?, ? )
            """, ( id, tag, ))
        
    return json.dumps(new_entry)

def update_entry(id, new_entry):
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
            UPDATE Journal_entries
                SET
                    concept = ?,
                    entry = ?,
                    moodId = ?,
                    date = ?
                WHERE id = ?
            """, (new_entry['concept'], new_entry['entry'], 
                new_entry['moodId'], new_entry['date'], id, ))
        
        rows_affected = db_cursor.rowcount
        
    if rows_affected == 0:
        return False
    else:
        return True