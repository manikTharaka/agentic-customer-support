from typing import Annotated
from langchain_experimental.utilities import PythonREPL

from langchain_openai import ChatOpenAI

from typing_extensions import TypedDict
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from load_env import load_env
from agents import get_product_details_node, get_review_node, get_orders_node, get_supervisor_node   

load_env()


members = ["product_review_agent", "product_details_agent","orders_agent"]

options = members + ["FINISH"]

system_prompt = f"""Your name is Frodo and you are a supervisor tasked with managing a conversation between the 
    following workers: {members}. Given the following user request,
     respond with the worker to act next. Each worker will perform a
     task and respond with their results and status. If you do not have the information that is required by a worker, query a relevant worker for the information. 
     When finished, respond with FINISH."""


llm = ChatOpenAI(model="gpt-4o")

supervisor_node = get_supervisor_node(llm, members, system_prompt)
product_review_node = get_product_details_node(llm)
product_details_node = get_review_node(llm)
order_details_node = get_orders_node(llm)

builder = StateGraph(MessagesState)
builder.add_edge(START, "supervisor")
builder.add_node("supervisor", supervisor_node)
builder.add_node("product_review_agent", product_review_node)
builder.add_node("product_details_agent", product_details_node)
builder.add_node("orders_agent", order_details_node)


graph = builder.compile()


for s in graph.stream(
    {"messages": [("user", "list all orders")]}, subgraphs=True
):
    if "product_details_agent" in s[1].keys():
        print(s[1]["product_details_agent"]["messages"][0].content)
        print("----")
    elif "product_review_agent" in s[1].keys():
        print(s[1]["product_review_agent"]["messages"][0].content)
        print("----")
    elif "orders_agent" in s[1].keys():
        print("orders_agent")
        print(s[1]["orders_agent"]["messages"][0].content)
        print("----")