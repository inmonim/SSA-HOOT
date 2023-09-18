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


# Token 생성 함수
def create_access_token(data: dict, expires_minutes: timedelta = ACCESS_TOKEN_EXPIRE_MINUTES):
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)

    # 클레임 데이터에 만료 시간 추가
    data.update({"exp": expire})

    # JWT 생성
    encoded_jwt = jwt.encode(data, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_token(data: dict, expires_minutes: timedelta = REFRESH_TOKEN_EXPIRE_MINUTES):
    expire = datetime.utcnow() + timedelta(expires_minutes)
    
    data.update({"exp": expire})
    
    encoded_jwt = jwt.encode(data, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
def verify_token(token: str, SECRET_KEY: str = ACCESS_SECRET_KEY, algorithm: str = ALGORITHM):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=algorithm)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="인증 실패")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다")
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="토큰 디코딩 실패")