from fastapi import FastAPI
from . import models
from .database import engine
from .routers import items,users, auth

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello WOrld!"}

app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)