
from context import PDFContextProvider
from langgraph.prebuilt import create_react_agent
from langgraph.graph import MessagesState
from langgraph.types import Command
from typing import Literal
from tools import orders_tool, orders_insert_tool
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict




def get_supervisor_node(llm, members,system_prompt):
    options = members + ["FINISH"]
    
    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: MessagesState) -> Command[Literal[*members, "__end__"]]:
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto)
    
    return supervisor_node

def get_review_node(llm):

    review_context_provider = PDFContextProvider("context_docs/Sleep Better Product Catalog.pdf")
    review_agent = create_react_agent(
        llm,
        tools=[],
        state_modifier="You are a product review provider. You are capable of providing user reviews,mattress reviews and feedback about mattresses. Use the following details as context:"
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
            # goto="supervisor",
        )

    return product_review_node

def get_product_details_node(llm):
    details_context_provider = PDFContextProvider("context_docs/Sleep Better Product Catalog.pdf")
    details_agent = create_react_agent(
        llm,
        tools=[],
        state_modifier="""You are a product details provider. 
        You are capable of providing product details such as price, product name and features. 
        Use the following context to answer user queries: """ 
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
            # goto="supervisor",
        )

    return product_details_node

def get_orders_node(llm):
    orders_agent = create_react_agent(
        llm,
        tools=[orders_tool,orders_insert_tool],
        state_modifier=""""You are a orders agent. You have access to a database of orders with the following schema:
    products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    size TEXT NOT NULL,
    height REAL NOT NULL,
    type TEXT NOT NULL
);

orders (
        id INTEGER PRIMARY KEY,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        status TEXT NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (id)
);

    Answer user queries about orders.You can execute SQL queries to fetch data from the orders table.
    convert the data in the dictionary to a human-readable format and return it to the user.

    You can add products to the products table and you can place orders by executing SQL queries to insert data into the orders table. The default status of the order is 'pending' 
    and the price is calculated based on the quantity and the product price, the product price can be retrieved from the products table.
    If you need more information about the product, you can route the conversation to the supervisor to obtain the necessary information.
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
            # goto="supervisor",
        )

    return order_details_node