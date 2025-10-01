# phase 1:

# 1. setup api keys for Groq and Tavily

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


# 2. setup llm and tools

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch  

openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

search_tool = TavilySearch(max_results=2)  

# 3. setup ai agent with search tool functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import HumanMessage

system_prompt = "Act as an AI Chatbot who is smart and friendly"
agent = create_react_agent(
    model=groq_llm,
    tools=[search_tool],
    prompt=system_prompt
)

query = "Tell me about the trends in crypto market"
state = {"messages": [HumanMessage(content=query)]}
response = agent.invoke(state)
messages = response.get("messages")
ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
print(ai_messages[-1])