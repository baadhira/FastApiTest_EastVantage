from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import engine,sessionLocal
from . import models,schemas,auth,address
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')

def Index():
    return {"message":"Hello world!"}




app.include_router(auth.router)
app.include_router(address.router)


