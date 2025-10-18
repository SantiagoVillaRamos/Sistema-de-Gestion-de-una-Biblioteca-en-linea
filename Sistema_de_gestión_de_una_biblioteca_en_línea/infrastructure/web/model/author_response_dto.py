from pydantic import BaseModel


class CreateAuthorCommand(BaseModel):
  
    name: str
    description: str

class CreateAuthorResponse(BaseModel):
   
    author_id: str
    name: str
    description: str
