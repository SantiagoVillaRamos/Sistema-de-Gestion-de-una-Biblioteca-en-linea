from pydantic import BaseModel
from typing import List, Optional

class CreateAuthorRequest(BaseModel):
  
    name: str
    description: str

class CreateAuthorResponse(BaseModel):
   
    author_id: str
    name: str
    description: str


class GetBooksResponse(BaseModel):
    
    isbn: str
    title: str
    author_names: List[str]
    description: str
    available_copies: int


class AuthorDetailResponse(BaseModel):
    
    author_id: str
    name: str
    description: str
    books: List[GetBooksResponse]
    
class UpdateAuthorRequest(BaseModel):
    # Usamos Optional para permitir actualizaciones parciales (si no se envía, no se modifica).
    name: Optional[str] = None
    description: Optional[str] = None