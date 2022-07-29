from pydantic import BaseModel
from typing import Optional

class SignupModel(BaseModel):
    id:Optional[int]
    username:str
    password:str

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"username",
                "password":"password"
            }
        }


# from pydantic import BaseModel
# from typing import Optional

class AddressBookBase(BaseModel):
    house_name: str
    pincode: str
    street_name: Optional[str]
    fulladdress: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    city: str


class AddressBookCreate(AddressBookBase):
    pass


class AddressBook(AddressBookBase):
    id: int
    owner_id = int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    addresses: list[AddressBook] = []

    class Config:
        orm_mode = True