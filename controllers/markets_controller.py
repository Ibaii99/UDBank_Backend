
from controllers.db_engine.database_engine import DatabaseEngine

class MarketsController:
    def __init__(self):
        self.db = DatabaseEngine()

    def get_all(self):
        return self.db.get_markets()

    def get_by_code(self, code:str):
        return self.db.get_market_by_code(code)
