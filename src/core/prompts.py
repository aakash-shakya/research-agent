from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Planner: Generate sub-questions
planner_prompt = ChatPromptTemplate([
    ("system", """You are a research planner. Given the original query and any prior notes,
    generate 3-5 non-overlapping sub-questions to explore gaps. Focus on multi-hop aspects.
    Output only the list of questions, one per line."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{original_query}\nPrior notes:{notes}")
])

# Researcher/QA Agent: Retrieve and answer
researcher_prompt = ChatPromptTemplate([
    ("system", """You are a factual researcher. Use the provided context or search tool to answer the current question succinctly.
    Append notes on unknowns/gaps and bookmark relevant excerpts. Be rigorous, no hallucinations.
    If needed, call the search tool."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "Current question: {current_question}\nContext: {context}")
])

# Picker/Director: Select next question
picker_prompt = ChatPromptTemplate([
    ("system", """You are a task director. From the list of unanswered sub-questions, select the most pertinent one
    to the original query. Output only the selected question."""),
    ("human", "Original: {original_query}\nUnanswered: {sub_questions}\nPrior notes: {notes}")
])

# Analyser/Manager: Check convergence
analyser_prompt = ChatPromptTemplate([
    ("system", """You are a research manager. Review the latest notes and iteration count. Decide if converged
    (enough depth, no major gaps). Output 'CONVERGE' or 'CONTINUE'."""),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "Iteration: {iteration}\nNotes: {notes}")
])

# Compiler: Synthesize final report
compiler_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a report compiler. Synthesize all notes and bookmarks into a comprehensive, cited answer
    to the original query. Structure: Introduction, Key Findings, Conclusion. Include citations."""),
    ("human", "Original: {original_query}\nAll notes: {notes}\nBookmarks: {bookmarks}")
])