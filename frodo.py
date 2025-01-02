import pprint
from typing import Annotated
from langchain_experimental.utilities import PythonREPL

from langchain_openai import ChatOpenAI
import uuid

from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from langchain_core.messages import HumanMessage
from load_env import load_env
from agents import get_product_details_node, get_review_node, get_orders_node, get_supervisor_node   

load_env()


members = ["product_review_agent", "product_details_agent","orders_agent"]

options = members + ["FINISH"]

system_prompt = f"""Your name is Frodo and you are a supervisor tasked with managing a conversation between the 
    following workers: {members}. Each worker is capable of performing the following tasks.
    product_review_agent: Provides user reviews,customer feedback,product reviews, mattress reviews, personal experience.
    product_details_agent: Provides details such as key features, Best usage and construction details about mattresses. 
    orders_agent: Capable of placing orders,querying database for product information and order information.
     respond with the worker to act next. Each worker will perform a task and respond with their results and status.
    If a worker requires extra information, you can route the conversation to another worker to obrain the necessary information and continue the conversation with the original worker. 
    When all workers have completed their tasks respond with FINISH to end the conversation."""


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


cached_human_responses = ["hi!", "rag prompt", "1 rag, 2 none, 3 no, 4 no", "red", "q"]
cached_response_index = 0
config = {"configurable": {"thread_id": str(uuid.uuid4())}}
FRODO = "Frodo"
while True:
    try:
        user = input("User (q/Q to quit): ")
    except:
        user = cached_human_responses[cached_response_index]
        cached_response_index += 1
        print(f"User (q/Q to quit): {user}")
    if user in {"q", "Q"}:
        print(f"{FRODO}: Thanks for using Frodo! Goodbye!")
        break
    output = None
    for output in graph.stream(
        {"messages": [HumanMessage(content=user)]}, config=config,
    ):
        if output.values() is not None:
            last_message = next(iter(output.values()))
            if last_message is not None:
                last_message = last_message["messages"][-1]
                # last_message.pretty_print()
                print(f"{FRODO}:{last_message.content}")
       
