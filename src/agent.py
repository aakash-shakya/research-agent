from langgraph.graph import StateGraph, END
from src.core.models import AgentState
from src.core.nodes import planner_node, researcher_node, picker_node, analyser_node, compiler_node
from src.utils import should_continue

def create_agent_graph():
    """Creates and compiles the research agent state graph."""
    
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("picker", picker_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyser", analyser_node)
    workflow.add_node("compiler", compiler_node)

    # Edges: Start -> planner -> picker -> researcher -> analyser -> conditional
    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "picker")
    workflow.add_edge("picker", "researcher")
    workflow.add_edge("researcher", "analyser")

    workflow.add_conditional_edges("analyser", should_continue, {"compiler": "compiler", "picker":"picker"})
    workflow.add_edge("compiler", END)

    # Compile graph
    app = workflow.compile()

    print('Graph compiled! Ready to run.')

    return app