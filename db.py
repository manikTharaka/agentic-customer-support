import sqlite3
from typing import List, Tuple
import logging
class Database:

    _instance = None
    def __init__(self, db_name: str):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row  # To return rows as dictionaries
        self.cursor = self.connection.cursor()
        logging.debug("Connected to database")

    @staticmethod
    def get_instance(db_name: str) -> 'Database':
        if Database._instance is None:
            Database._instance = Database(db_name)
        return Database._instance

    def execute(self, query: str, params: Tuple = ()):
        self.cursor.execute(query, params)
        self.connection.commit()
        logging.debug(f"executed query: {query}")

    def fetchall(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        results = []
        for row in rows:
            results.append(dict(row))
        
        logging.debug("fetched results")
        return results
    

    def fetchone(self, query: str, params: Tuple = ()) -> sqlite3.Row:
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
