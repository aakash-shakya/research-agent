from src.core.models import AgentState
from langchain_core.messages import HumanMessage
from src.agent import create_agent_graph
from src.config import Config

print("HEY THERE! I am Deep Research Agent, ready to assist you with in-depth research.\n Ask me anything!")
user_query = input('Enter what you want to know about: ')

initial_state = AgentState(messages=[HumanMessage(content=user_query)],
                           original_query=user_query,
                           sub_questions=[],
                           current_question="",
                           notes=[],
                           bookmarks=[],
                           iteration=0,
                           max_iterations=3,
                           converged=False
                        )

config = Config.get_config()

app = create_agent_graph()
result = app.invoke(initial_state, config=config)

final_report = result["messages"][-1].content

print("Final Research Report: \n")
print(final_report)