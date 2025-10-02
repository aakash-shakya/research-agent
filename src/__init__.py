from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0.1, convert_system_message_to_human=True)
search_tool = TavilySearch(max_results=5)