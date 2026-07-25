from fastapi import APIRouter,Depends,Form,Response
from pydantic import BaseModel,Field
from Database.ds import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from Tokens.GenerateTokens import generate_secure_token
from password.generate import hashpassword,verifypassword
import bcrypt
from Models.md import User,UserRole
router=APIRouter(
    prefix="/auth",
    tags=["auth"]
)
class createUserRequest(BaseModel):
    email:str
    password:str
    role:UserRole=UserRole.USER

db_dependency = Annotated[Session, Depends(get_db)]

 
@router.post("/create_user")
async def create_user(db:db_dependency, user_request:createUserRequest):
    print(user_request.role)
    print(type(user_request.role))
    create_user_model= User(
        email=user_request.email,
        password= hashpassword(user_request.password),
        role= user_request.role
    )
    db.add(create_user_model)
    db.commit()

def authenticate(password:str,email:str, db:Session):
    exist_user= db.query(User).filter(User.email==email).first()
    print("user in authenticate",exist_user.password)
    if not exist_user:
        return False
    if not verifypassword(password, exist_user.password):
        return False
    return exist_user



@router.post("/login")
async def login( db: db_dependency,response:Response,email:str=Form(...), password:str=Form(...)):
    user= authenticate(password,email,db)
    print(user.id, user.email, user.role,",user in login")
    access_token= generate_secure_token(user, 15,False)
    refresh_token= generate_secure_token(user, 7,True)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age= 5*60
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
       
        max_age=7 * 24 * 60 * 60
    )
    return {"message":"login successfully", "success":True}
    




    

    

  


 






    


