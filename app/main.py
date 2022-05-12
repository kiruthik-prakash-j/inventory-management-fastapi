from fastapi import FastAPI
from . import models
from .database import engine
from .routers import items,users, auth
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)

origins = ["*"]
    
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello WOrld!"}

app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth.router)