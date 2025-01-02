import pprint
from typing import Annotated
from langchain_experimental.utilities import PythonREPL

from langchain_openai import ChatOpenAI

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
     task and respond with their results and status.The workers are capable of providing the following services:
        - product_review_agent: Provide a review for a product.
        - product_details_agent: Provide details for a product. 
        - orders_agent: Capable of placing orders,querying database for product information and order information.
    
    If a worker does not return a response with FINAL status and requires extra information, you can route the conversation to another worker to obrain the necessary information and continue the conversation with the original worker. When all workers have completed their tasks, respond with FINISH to end the conversation."""


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
    {"messages": [("user", """Insert the following product information to the products table:1. Ultra Comfort Mattress
Price: $1,299 (Queen) Type: Hybrid (Memory Foam + Pocket Coils) Height: 12 inches
Construction Layers:
●
●
●
●
2" Cooling Gel Memory Foam Top Layer
2" Responsive Comfort Foam
2" Transition Layer
6" Pocket Coil System (1,024 coils in Queen size)
Key Features:
●
●
●
●
●
●
Advanced temperature regulation with cooling gel technology
Edge-to-edge support system
Motion isolation technology
Breathable quilted cover with silver-infused fibers
CertiPUR-US® certified foams
Compatible with adjustable bed bases
Best For:
●
●
●
●
Hot sleepers
Couples
Back and stomach sleepers
Those needing extra edge support
Available Sizes: Twin, Twin XL, Full, Queen, King, California King Warranty: 15 years Trial
Period: 100 nights""")]}, subgraphs=True
):
    # if "product_details_agent" in s[1].keys():
    #     print(s[1]["product_details_agent"]["messages"][0].content)
    #     print("----")
    # elif "product_review_agent" in s[1].keys():
    #     print(s[1]["product_review_agent"]["messages"][0].content)
    #     print("----")
    # elif "orders_agent" in s[1].keys():
    #     print("orders_agent")
    #     print(s[1]["orders_agent"]["messages"][0].content)
    #     print("----")

    pprint.pprint(s)
    print("\n\n")