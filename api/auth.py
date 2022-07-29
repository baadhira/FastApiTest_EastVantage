from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from . import models,schemas
from .schemas import SignupModel
from .database import sessionLocal,engine
from fastapi import APIRouter
from .models import User
router=APIRouter(
    prefix='/auth',
    tags=['auth']
)

session=sessionLocal(bind=engine)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

"Signup for user"
@router.post('/signup',response_model=SignupModel,status_code=status.HTTP_201_CREATED)
async def signup(user:SignupModel):
    db_username=session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="User with the username address already exists"
        )
    fake_hashed_password = user.password + "encrypt fakely"
    
    new_user=User(
        username=user.username,
        password=fake_hashed_password

        

    )
    print("password",type(new_user.password))
    session.add(new_user)
    session.commit()
    return new_user

"Return user according to given id"
@router.get('/user/{id}',status_code=status.HTTP_200_OK)
def get_user(id:int,db:Session=Depends(get_db)):
    myuser=db.query(models.User).filter(models.User.id==id).first()
    if myuser:
        return myuser

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The user doesnot exist")