
from controllers.db_engine.database_engine import DatabaseEngine
from logic.user import User

class UsersController:
    def __init__(self):
        self.db = DatabaseEngine()

    def is_password_correct(self, username: str, password:str):
        return self.db.is_password_correct(username, password)

    def save(self, user: User):
        return self.db.save_user(user)

    def get(self, username: str):
        return self.db.get_user(username)
    
    def modify(self, username: str, password: str, user: User):
        return self.db.modify_user(username, password, user)
