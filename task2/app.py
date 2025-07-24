from langchain.memory import ConversationBufferMemory
from langgraph.graph import StateGraph, END
from typing import Dict, Any
from pydantic import BaseModel

# Define the state schema to hold query, context, and results
class WorkflowState(BaseModel):
    query: str
    context: str
    segment: str
    suggestion: str

# Initialize memory to persist conversation context
memory = ConversationBufferMemory()

# Node 1: Capture Query and Retrieve Context
def query_capture_node(state: WorkflowState) -> Dict[str, Any]:
    """Captures the user query and retrieves conversation context."""
    # Simulate retrieving past context from memory
    past_context = memory.load_memory_variables({}).get("history", "")
    updated_context = f"{past_context}\nUser Query: {state.query}"
    memory.save_context({"input": state.query}, {"output": "Query received"})
    return {"context": updated_context}

# Node 2: Customer Segmentation (Mock PCI Logic)
def segmentation_node(state: WorkflowState) -> Dict[str, Any]:
    """Segments the customer based on query keywords (mock PCI)."""
    query = state.query.lower()
    # Mock segmentation logic based on keywords
    if "urgent" in query or "problem" in query:
        segment = "High-Priority Customer"
    elif "buy" in query or "purchase" in query:
        segment = "Potential Buyer"
    else:
        segment = "General Inquirer"
    return {"segment": segment}

# Node 3: Generate Suggestion
def suggestion_node(state: WorkflowState) -> Dict[str, Any]:
    """Generates a suggestion based on segment and context."""
    segment = state.segment
    # Mock suggestion logic
    if segment == "High-Priority Customer":
        suggestion = "Offer immediate support ticket escalation."
    elif segment == "Potential Buyer":
        suggestion = "Recommend our premium product with a 10% discount."
    else:
        suggestion = "Provide general product information and FAQ link."
    return {"suggestion": suggestion}

# Define the LangGraph workflow
def build_workflow():
    workflow = StateGraph(WorkflowState)
    
    # Add nodes
    workflow.add_node("query_capture", query_capture_node)
    workflow.add_node("segmentation", segmentation_node)
    workflow.add_node("suggestion", suggestion_node)
    
    # Define edges (flow between nodes)
    workflow.set_entry_point("query_capture")
    workflow.add_edge("query_capture", "segmentation")
    workflow.add_edge("segmentation", "suggestion")
    workflow.add_edge("suggestion", END)
    
    # Compile the graph
    return workflow.compile()

# Run the workflow
def run_workflow(query: str):
    app = build_workflow()
    initial_state = WorkflowState(
        query=query, context="", segment="", suggestion=""
    )
    result = app.invoke(initial_state)
    return result

if __name__ == "__main__":
    print(" PCI Query Flow Chatbot")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("🔹 Enter your query: ")

        if user_query.strip().lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break

        result = run_workflow(user_query)
        print(f"\n Context:\n{result['context']}")
        print(f" Segment: {result['segment']}")
        print(f" Suggestion: {result['suggestion']}\n")
