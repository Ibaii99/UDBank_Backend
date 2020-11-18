
from controllers.db_engine.database_engine import DatabaseEngine

class SessionsController:
    def __init__(self):
        self.db = DatabaseEngine()

    def save(self, session_data):
        return self.db.save_session(session_data)
        
    def get(self, session):
        return self.db.get_session(session)

    def remove(self, session):
        return self.db.remove_session(session)