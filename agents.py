
from context import PDFContextProvider
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from tools import orders_tool, orders_insert_tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal[*options]

def get_supervisor_node(llm, members,system_prompt):

    def supervisor_node(state: MessagesState) -> Command[Literal[*members, "__end__"]]:
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto)

def get_review_node(llm):

    review_context_provider = PDFContextProvider("context_docs/Sleep Better Product Catalog.pdf")
    review_agent = create_react_agent(
        llm,
        tools=[],
        state_modifier="You are a product review provider. Provide the product review for the requseted product.  Use the following details as context:"
        + review_context_provider.get_context(),
    )

    def product_review_node(state: MessagesState) -> Command[Literal["supervisor"]]:
        result = review_agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(content=result["messages"][-1].content, name="review_provider")
                ]
            },
        )

    return product_review_node

def get_product_details_node(llm):
    details_context_provider = PDFContextProvider("context_docs/Sleep Better Product Catalog.pdf")
    details_agent = create_react_agent(
        llm,
        tools=[],
        state_modifier="You are a product details provider. Provide the product details for the requested product. Use the following details as context: "
        + details_context_provider.get_context(),
    )

    def product_details_node(state: MessagesState) -> Command[Literal["supervisor"]]:
        result = details_agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content, name="details_provider"
                    )
                ]
            },
        )

    return product_details_node

def get_orders_node(llm):
    orders_agent = create_react_agent(
        llm,
        tools=[orders_tool,orders_insert_tool],
        state_modifier=""""You are a orders agent. You have access to a database of orders with the following schema:
    orders (
            id integer PRIMARY KEY,
            product_name text NOT NULL,
            quantity integer NOT NULL,
            status text NOT NULL,
            price real NOT NULL);

    Answer user queries about orders.You can execute SQL queries to fetch data from the orders table.
    convert the data in the dictionary to a human-readable format and return it to the user.

    You can place orders by executing SQL queries to insert data into the orders table. The default status of the order is 'pending' 
    and the price is calculated based on the quantity and the product price, the product price can be retrieved from the product details.
    """
    )



    def order_details_node(state: MessagesState) -> Command[Literal["supervisor"]]:
        result = orders_agent.invoke(state)
        return Command(
            update={
                "messages": [
                    HumanMessage(
                        content=result["messages"][-1].content, name="orders"
                    )
                ]
            },
        )

    return order_details_node