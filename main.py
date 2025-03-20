from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import database
from pydantic import BaseModel

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Key/Value Store API")


# Pydantic models for request/response
class KeyValueCreate(BaseModel):
    value: str


class KeyValueResponse(BaseModel):
    key: str
    value: str

    class Config:
        from_attributes = True


# CRUD operations
@app.post("/kv/{key}", response_model=KeyValueResponse)
def create_or_update_value(
    key: str, kv: KeyValueCreate, db: Session = Depends(database.get_db)
):
    db_item = (
        db.query(models.KeyValue).filter(models.KeyValue.key == key).first()
    )
    if db_item:
        db_item.value = kv.value
    else:
        db_item = models.KeyValue(key=key, value=kv.value)
        db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/kv/{key}", response_model=KeyValueResponse)
def read_value(key: str, db: Session = Depends(database.get_db)):
    db_item = (
        db.query(models.KeyValue).filter(models.KeyValue.key == key).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_item


@app.get("/kv/", response_model=List[KeyValueResponse])
def list_keys(db: Session = Depends(database.get_db)):
    return db.query(models.KeyValue).all()


@app.delete("/kv/{key}")
def delete_value(key: str, db: Session = Depends(database.get_db)):
    db_item = (
        db.query(models.KeyValue).filter(models.KeyValue.key == key).first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Key not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Key deleted successfully"} 