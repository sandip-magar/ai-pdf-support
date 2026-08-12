import os 
from dotenv import load_dotenv
import bcrypt
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta, timezone
from jose import jwt

load_dotenv()

oauth_schema = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTE"))

def hash_password(plain_password: str) -> bytes:
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password: str, hashed_password) -> bool:
    #convert bytes if it's on string.
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token:str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credientals",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )