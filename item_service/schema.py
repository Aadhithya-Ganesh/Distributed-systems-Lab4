from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int

class ItemOut(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
