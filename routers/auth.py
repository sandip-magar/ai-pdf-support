from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import hash_password, verify_password, create_access_token, decode_token, oauth_schema
from db.models import User
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from db.database import get_db
from db.schemas import UserCreate, UserResponse, UserUpdate, Token
import sys
sys.path.append("..")

router = APIRouter()

#register the user 
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #hash the password for the new_user
    hashed_password = hash_password(user.password).decode('utf-8')
    #create a new user
    new_user = User(
        username = user.username,
        hashed_password = hashed_password,
        is_active = user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#login for the user 
@router.post("/login", response_model=Token)
async def login_user(credientals: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    existing_user = db.query(User).filter(User.username == credientals.username).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(credientals.password, existing_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password or Username",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not existing_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User Account is inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data= {"sub": existing_user.username})

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }

#This is the protected route 
@router.get("/me", response_model=UserResponse)
async def get_current_user(credientals : HTTPAuthorizationCredentials = Depends(oauth_schema), db: Session = Depends(get_db)): 
    token = credientals.credentials
    username = decode_token(token)
    #search for the user 
    user = db.query(User).filter(User.username == username).first()
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user 

#this is optional but useful 
@router.post("/me", response_model=Token)
async def get_new_access_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_access_token = create_access_token(data= {"sub": current_user.username})

    return {
        "access_token": new_access_token,
        "token_type": "Bearer"
    }