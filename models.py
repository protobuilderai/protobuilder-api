from sqlalchemy import Column, String, Text
from database import Base


class KeyValue(Base):
    __tablename__ = "key_value_store"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text) 