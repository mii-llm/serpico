
from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str  
    content: str
    id: Optional[str] 
