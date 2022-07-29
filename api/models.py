from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    username=Column(String(100),unique=True)
    password=Column(String(1000),unique=True)
    addresses=relationship("Address",back_populates="user")


class Address(Base):
    __tablename__="addresses"
    id=Column(Integer,primary_key=True,autoincrement=True)
    house_name=Column(String(100))
    pincode=Column(String(50))
    street_name=Column(String(100))
    city=Column(String(100))
    fulladdress=Column(String(300))
    latitude=Column(String(100))
    longitude=Column(String(100))
    user_id=Column(Integer,ForeignKey("users.id"))
    user=relationship("User",back_populates="addresses")