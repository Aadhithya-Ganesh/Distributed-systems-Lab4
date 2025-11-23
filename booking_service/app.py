from fastapi import FastAPI
from database import init_db
from booking import router as bookingRouter

app = FastAPI()

init_db()

@app.get("/")
def hello():
    return {"message" : "hello from order"}

app.include_router(bookingRouter)