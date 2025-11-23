from pydantic import BaseModel

class BookingCreate(BaseModel):
    customer_name: str
    item_id: int
    quantity: int
    status: str

class BookingOut(BaseModel):
    booking_id: int 
    customer_name: str
    item_id: int
    quantity: int
    total_price: float
    status: str