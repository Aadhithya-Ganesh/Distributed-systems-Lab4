from sqlalchemy import Column, Integer, String, Float
from database import Base

class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    item_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False)