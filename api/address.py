from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from . import models,schemas

from .database import sessionLocal,engine

session=sessionLocal(bind=engine)


router=APIRouter(
    prefix='/address',
    tags=['address']
)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user(db: Session, user_id: int):
    """Returns the User based on the given id"""
    return db.query(models.User).filter(models.User.id == user_id).first()

"""Returns the GeoLocation (Address, Latitude and Longitude of a given place."""
def get_location(city_name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name)
    return getLoc

"returns latitude and lattitude of city passed as parameter"
def get_coordinates(city_name):
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city_name)
    return getLoc.latitude, getLoc.longitude

"user creating address"
def create_user_address(db: Session, address: schemas.AddressBookCreate, user_id: int):
    location = get_location(address.city)
    if location:
        address.fulladdress = str(location)
        address.latitude = str(location.latitude)
        address.longitude = str(location.longitude)
        db_address = models.Address(**address.dict(), user_id=user_id)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address
    else:
        raise HTTPException(
            status_code=404, detail="Please enter a valid city name")

"""Creates an address for the user. A user can create multiple addresses
    Location and address fields will be autopopulated"""        
@router.post("/users/{user_id}/addresses/", response_model=schemas.AddressBook)
def create_address_for_user(user_id: int, address: schemas.AddressBookCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_user_address(db=db, address=address, user_id=user_id)

"""Returns the Address based on the given id"""
def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

"""Accepts city names and returns the distance between the cities based on the location coordinates"""
def calculate_distance(city1: str, city2: str):
    city1 = get_coordinates(city1)
    city2 = get_coordinates(city2)
    distance = geodesic(city1, city2).km
    return distance

"""Accepts an address id, and distance in Kilometers. Returns a list of addresses found within this distance"""
def get_nearby_addresses(address_id: int, distance_in_km: int, db: Session):
    user_input_address = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    user_input_city = user_input_address.city
    all_addresses = db.query(models.Address).all()
    selected_addresses = []
    for address in all_addresses:
        if address_id != address.id:
            calculated_distance = calculate_distance(
                user_input_city, address.city)
            if calculated_distance < distance_in_km:
                selected_addresses.append(address)
    return selected_addresses

"""Returns a list of all saved addresses"""
def get_addresses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Address).offset(skip).limit(limit).all()

"""Returns a list of all the addresses in the database"""
@ router.get("/addresses/", response_model=list[schemas.AddressBook])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    addresses = get_addresses(db, skip=skip, limit=limit)
    return addresses

"""Returns a list of all the nearby addresses in the database, within the given distance parameter"""
@ router.post("/nearby_addresses/")
def find_nearby_addresses(address_id: int, distance_in_km: int, db: Session = Depends(get_db)):
    
    db_address = get_address(db, address_id=address_id)
    if db_address is None:
        raise HTTPException(
            status_code=404, detail="The given address id is not found. Pleases re-enter.")
    nearby_addresses = get_nearby_addresses(
        address_id, distance_in_km, db)
    return nearby_addresses