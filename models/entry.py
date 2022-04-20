class Journal_entries(): # Use Pascal case for classes and should always be singular (it makes ONE object)
    """This class is the model for fetching entries from the database"""
    
    def __init__(self, id, concept, entry, moodId, date, mood = None, tags = []):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.moodId = moodId
        self.date = date
        self.mood = mood
        self.tags = tags