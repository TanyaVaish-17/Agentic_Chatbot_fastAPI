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






# 3. Run app and explore swagger ui docs