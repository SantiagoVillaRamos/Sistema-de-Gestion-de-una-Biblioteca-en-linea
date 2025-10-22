
from pydantic import BaseModel, EmailStr, Field

class MessageResponse(BaseModel):
    
    message: str




class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)

class LoginResponse(BaseModel):
    token: str
    token_type: str = "bearer"