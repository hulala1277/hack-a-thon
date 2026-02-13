from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .common import TimestampModel

class IssueCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str

class IssueOut(TimestampModel):
    id: UUID
    title: str
    description: Optional[str]
    category: str
    location: str
    status: str
    upvotes: int
    downvotes: int