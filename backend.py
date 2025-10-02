# Phase 2:

# 1. Setup pydantic model (scheme validation)
from pydantic import BaseModel                     # data validation library that ensures data is correct & in right format
class RequestState(BaseModel):                     # It's basically for frontend to know that in which format it has to send data
    model_name:str                                 # And for backend to know in which format it have to receive data.
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool


# 2. Setup ai agent from frontend request
from fastapi import FASTAPI
from ai_agent import get_response_from_ai_agent

ALLOWED_MODEL_NAMES=["llama3-70b-8192", "mixtral-8x7b-32768", "llama-3.3-70b-versatile", "gpt-4o-mini"]

#Now we have to set up our app for backend to manage the frontend request
app=FastAPI(title="Langchain AI Agent")

@app.post("/chat")  # it is the end point where the frontend request is received

def chat_endpoint(request:RequestState):  # Request processing and also the the request received must be of class RequestState type
     if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error": "Invalid model name. Kindly select a valid AI model"}

    # These all we will get from frontend

    llm_id=request.model_name
    query=request.messages
    allow_search=request.allow_search
    system_prompt=request.system_prompt
    provider=request.model_provider

    # Creating AI agent to get response from it
    response=get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider)
    return response

# 3. Run app and explore swagger ui docs

# Now we have to host it using uvicorn
