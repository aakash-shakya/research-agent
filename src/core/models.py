from typing import List, TypedDict, Annotated
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage], add_messages]
    original_query: str
    sub_questions: List[str]
    current_question: str
    notes: List[str]
    bookmarks: List[str]
    iteration: int
    max_iterations: int
    converged: bool