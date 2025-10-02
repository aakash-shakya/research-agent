from src.core.models import AgentState

def format_docs(docs):
    """Format retrieved docs into a single string for context."""
    return "\n\n".join([doc.page_content for doc in docs])

def should_continue(state:AgentState) -> str:
    if state['converged'] or not state['sub_questions']:
        return "compiler"
    return "picker"