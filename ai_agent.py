# phase 1:
# 1. setup api keys for Groq and Tavily

import os
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")


# 2. setup llm and tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

openai_llm=ChatOpenAI(model=gpt-4o-mini)
groq_llm=ChatGroq(model=llama-3.3-70b-versatile)

search_tool=TavilySearchResults(max_results=2)
# 3. setup ai agent with search tool functionality

