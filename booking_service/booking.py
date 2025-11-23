from typing import Annotated, List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import requests
from database import SessionLocal
from model import Booking
from schema import BookingCreate, BookingOut

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/booking", tags=["booking"])

@router.post("/", response_model=BookingOut, status_code=201)
def create_booking(body: BookingCreate, db: db_dependency):
    # First, get the item from items service
    item = None
    try:
        response = requests.get(f"http://item-service:8080/items/{body.item_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Item not found")
        
        item = response.json()
        
        # Check if enough quantity is available
        if item['quantity'] < body.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Not enough items available. Available: {item['quantity']}, Requested: {body.quantity}"
            )
        
        # Calculate new quantity
        new_quantity = item['quantity'] - body.quantity
        
        # Update item quantity in items service
        update_data = {
            "name": item['name'],
            "description": item['description'],
            "price": item['price'],
            "quantity": new_quantity
        }
        
        update_response = requests.put(
            f"http://item-service:8080/items/{body.item_id}",
            json=update_data
        )
        
        if update_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to update item quantity")
        
        # If quantity becomes 0, you might want to delete the item (optional)
        # if new_quantity == 0:
        #     requests.delete(f"http://item-service:8000/items/{body.item_id}")
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Items service unavailable {e}")
    
    print(item)

    totalprice = body.quantity * item["price"]
    # Create booking
    booking = Booking(
        customer_name=body.customer_name,
        item_id=body.item_id,
        quantity=body.quantity,
        total_price=totalprice,
        status=body.status,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.get("/", response_model=List[BookingOut])
def get_all_bookings(db: db_dependency):
    return db.query(Booking).all()

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking_by_id(booking_id: int, db: db_dependency):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/{booking_id}", response_model=BookingOut)
def update_booking(booking_id: int, body: BookingCreate, db: db_dependency):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking.customer_name = body.customer_name
    booking.item_id = body.item_id
    booking.quantity = body.quantity
    booking.total_price = body.total_price
    booking.status = body.status

    db.commit()
    db.refresh(booking)
    return booking

@router.delete("/{booking_id}", response_model=BookingOut)
def delete_booking(booking_id: int, db: db_dependency):
    booking = db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return booking