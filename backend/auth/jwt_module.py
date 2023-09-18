import jwt
import yaml
from datetime import timedelta, datetime
from fastapi import HTTPException


# SECRET_KEY 불러오기
with open('config.yaml', 'r') as cf:
    secret_keys = yaml.safe_load(cf)
    ACCESS_SECRET_KEY = secret_keys['ACCESS_SECRET_KEY']
    REFRESH_SECRET_KEY = secret_keys['REFRESH_SECRET_KEY']

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 360


# Refresh Token 생성 함수
def create_refresh_token(data: dict, expires_minutes: timedelta = REFRESH_TOKEN_EXPIRE_MINUTES):
    
    expire = datetime.utcnow() + timedelta(expires_minutes)
    data.update({"exp": expire})

    refresh_jwt = jwt.encode(data, key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
    return refresh_jwt


# Access Token 생성 함수
def create_access_token(data: dict, refresh_token: str, expires_minutes: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES):
    
    # 리프레시 토큰 검증
    verify_token(refresh_token, secret_key=REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data.update({"exp": expire})
    
    access_jwt = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    return access_jwt


# 토큰 검증 함수
# 기본적으로 엑세스 토큰 검증을 토대로 기본값 구성. 리프레시 토큰 검증을 위해서는 secret_key 지정 필요
def verify_token(token: str, secret_key: str = ACCESS_SECRET_KEY, algorithm: str = ALGORITHM):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="인증 실패")
        return user_id
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="세션이 만료되었습니다.")
    
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="토큰이 올바르지 않습니다.")