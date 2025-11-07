# phase 1:

from dotenv import load_dotenv
load_dotenv()

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

# 3. setup ai agent with search tool functionality

from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import HumanMessage, SystemMessage

system_prompt = "Act as an AI Chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)
    tools = [TavilySearch(max_results=2)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt
    )
    if not isinstance(query, str):
        query = str(query)
    # query = "Tell me about the trends in crypto market"
    state = {
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
    }
    response = agent.invoke(state)
    messages = response.get("messages")
    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]
    return (ai_messages[-1]) if ai_messages else "No response"