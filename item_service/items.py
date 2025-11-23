from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from schema import ItemCreate, ItemOut
from model import Items
from typing import List


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemOut, status_code=201)
def addItems(body: ItemCreate, db: db_dependency):
    item = Items(name=body.name, description=body.description, price=body.price, quantity=body.quantity)
    db.add(item)
    db.commit() 
    db.refresh(item)
    return item

@router.get("/", response_model=List[ItemOut])
def getAllItems(
    db: db_dependency,
):
    query = db.query(Items)
    return query.all()

@router.get("/{itemId}", response_model=ItemOut)
def getItemByid(itemId : int, db: db_dependency):
    item = db.get(Items, itemId)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{itemId}", response_model=ItemOut)
def update_item(itemId: int, body: ItemCreate, db: db_dependency):
    item = db.get(Items, itemId)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = body.name
    item.description = body.description
    item.price = body.price
    item.quantity = body.quantity

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{itemId}", response_model=ItemOut)
def delete_item(itemId: int, db: db_dependency):
    item = db.get(Items, itemId)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return item
