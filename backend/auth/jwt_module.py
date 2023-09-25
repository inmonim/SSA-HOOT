from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
import yaml
from datetime import timedelta, datetime

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


# SECRET_KEY 불러오기
with open('config.yaml', 'r') as cf:
    secret_keys = yaml.safe_load(cf)
    ACCESS_SECRET_KEY = secret_keys['ACCESS_SECRET_KEY']
    REFRESH_SECRET_KEY = secret_keys['REFRESH_SECRET_KEY']

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 360


# Refresh Token 생성 함수
def create_refresh_token(data: dict):
    
    # 토큰 만료 시간 설정
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})

    # 토큰 생성
    refresh_jwt = jwt.encode(data, key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
    return refresh_jwt


# Access Token 생성 함수
def create_access_token(data: dict, refresh_token: str):
    
    # 리프레시 토큰 검증
    verify_refresh_token(refresh_token)
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    
    access_jwt = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    return access_jwt


# 토큰 검증 함수
def verify_token(token: str = Depends(oauth2_scheme)):
    
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="토큰이 없습니다.")
        
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="인증 실패")
        return user_id
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="세션이 만료되었습니다.")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="토큰이 올바르지 않습니다.")
    


def verify_refresh_token(token: str = Depends(oauth2_scheme)):
    
    try:
        if token is None:
            raise HTTPException(status_code=401, detail="토큰이 없습니다.")
        
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="인증 실패")
        return user_id
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="세션이 만료되었습니다.")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="토큰이 올바르지 않습니다.")