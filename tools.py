from db import Database
from langchain_core.tools import tool


@tool
def orders_tool(query: str):
    """
    Tool to query the database and retrieve order information.
    """
    db = Database.get_instance("mattress.db")
    return db.fetchall(query)

@tool
def orders_insert_tool(query: str):
    """
    Tool insert records to database.
    """
    db = Database.get_instance("mattress.db")
    return db.execute(query)