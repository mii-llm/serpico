from typing import Annotated, Literal

from pydantic import BaseModel

class Plan(BaseModel):
    title: str  
    description: str
    status: Literal['created', 'pending','finish'] 