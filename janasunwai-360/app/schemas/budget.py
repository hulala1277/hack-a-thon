from pydantic import BaseModel
from uuid import UUID

class BudgetCreate(BaseModel):
    sector: str
    fiscal_year: str
    allocated_amount: float

class BudgetOut(BudgetCreate):
    id: UUID
