from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage
from src.core.models import AgentState
from src.core.prompts import planner_prompt, researcher_prompt, picker_prompt, analyser_prompt, compiler_prompt
from src import llm, search_tool
from services.database_service import get_retriever_from_collection
from src.utils import format_docs

retriever = get_retriever_from_collection(collection="research_agent_pdf_collection", k=5)

def planner_node(state:AgentState) -> AgentState:
    """Generate sub-questions if none exist."""
    if not state.get('sub_questions'):
        chain = planner_prompt | llm | StrOutputParser()
        response = chain.invoke({
            "messages": state.get('messages'),
            "original_query": state.get('original_query'),
            "notes": state.get('notes')
        })
        sub_questions = [q.strip() for q in response.split('\n') if q.strip()]
        state['sub_questions'] = sub_questions
        state['messages'].append(AIMessage(content=f"Generated sub-questions: {sub_questions}"))

    return state

def researcher_node(state: AgentState) -> AgentState:
    """Retrieve context and answer current question."""
    # Fixed RAG chain: Use itemgetter to feed only query to retriever
    rag_chain = (
        {
            "context": itemgetter("current_question") | retriever | format_docs,
            "current_question": itemgetter("current_question"),
            "messages": itemgetter("messages")
        }
        | researcher_prompt
        | llm.bind_tools([search_tool])  # Bind tool for web search if needed
        | StrOutputParser()
    )

    response = rag_chain.invoke({
        "messages": state["messages"],
        "current_question": state["current_question"]
    })

    # Parse response (assume: answer + notes + bookmarks; in prod, use structured parser)
    notes = [response]  # Simplified; extract gaps/unknowns from response
    bookmarks = ["Sample citation from corpus"]  # Enhance with retriever metadata (e.g., doc.metadata['source'])

    state["notes"].extend(notes)
    state["bookmarks"].extend(bookmarks)
    state["messages"].append(AIMessage(content=response))
    return state

def picker_node(state: AgentState) -> AgentState:
    """Select next sub-question."""
    if state["sub_questions"]:
        chain = picker_prompt | llm | StrOutputParser()
        response = chain.invoke({
            "original_query": state["original_query"],
            "sub_questions": state["sub_questions"],
            "notes": "\n".join(state["notes"])
        })
        state["current_question"] = response
        # Remove selected from list (simplified: pop first match)
        state["sub_questions"] = [q for q in state["sub_questions"] if q != response]
        state["messages"].append(AIMessage(content=f"Selected: {response}"))
    return state

def analyser_node(state: AgentState) -> AgentState:
    """Check if converged."""
    state["iteration"] += 1
    chain = analyser_prompt | llm | StrOutputParser()
    decision = chain.invoke({
        "messages": state["messages"],
        "iteration": state["iteration"],
        "notes": "\n".join(state["notes"])
    }).strip().upper()

    state["converged"] = (decision == "CONVERGE") or (state["iteration"] >= state["max_iterations"])
    state["messages"].append(AIMessage(content=f"Decision: {decision}"))
    return state

def compiler_node(state: AgentState) -> AgentState:
    """Compile final report."""
    chain = compiler_prompt | llm | StrOutputParser()
    report = chain.invoke({
        "original_query": state["original_query"],
        "notes": "\n".join(state["notes"]),
        "bookmarks": state["bookmarks"]
    })
    state["messages"].append(AIMessage(content=report))
    return state