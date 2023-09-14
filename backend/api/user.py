from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr

import bcrypt
import re

from db_conn import session_open

from models.model import User

class CreateUser(BaseModel):
    user_name : str
    user_id : str
    password: str
    role : str

router = APIRouter()

# 계정 생성 요청
@router.post("/create_user")
async def create_user(request: Request, request_data: CreateUser):
    user_data = await request_data
    
    user_name = user_data['user_name']
    user_id = user_data['user_id']
    plain_pw = user_data['password']
    
    role = user_data.get('role')
    
    # user_id 재검사
    check_id_response = check_valid_id(user_id)
    if check_id_response['status_code'] != 200:
        return JSONResponse(content = check_id_response['content'],
                            status_code = check_id_response['status_code'])
        
    # 비밀번호 유효성 검사
    check_pw_response = check_valid_password(plain_pw)
    if check_pw_response['status_code'] != 200:
        return JSONResponse(content = check_pw_response['content'],
                            status_code = check_pw_response['status_code'])
    
    # 평문 비밀번호 암호화
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), salt)
    
    with session_open() as db:
        
        user = User()
        user.user_id = user_id
        user.name = user_name
        user.password = hashed_pw
        user.role = role
        db.add(user)
        db.commit()
    
    return JSONResponse(content = {'message':'계정이 생성되었습니다.'},
                        status_code = 200)

# 아이디 유효성 검사 요청
@router.post('/create_user/check_valid_id')
async def check_valid_id_request(request:Request):
    
    data = await request.json()
    
    user_id = data['user_id']
    
    id_check_response = check_valid_id(user_id)
    
    return JSONResponse(content=id_check_response['content'],
                        status_code=id_check_response['status_code'])

# 로그인 요청
@router.post('/login')
async def login(reqeust:Request):
    
    data = await reqeust.json()
    
    input_id = data['user_id']
    input_pw = data['password']
    
    with session_open() as db:
        
        user = db.query(User).filter(User.user_id == input_id).first()
        
        if not user:
            return JSONResponse(content={'message':'계정이 없습니다.'},
                                status_code=401)
        
        hashed_pw = user.password
        
        if bcrypt.checkpw(input_pw.encode('utf-8'), hashed_pw.encode('utf-8')) == False:
            return JSONResponse(content={'message':'비밀번호가 틀렸습니다.'},
                                status_code=401)
    
    return JSONResponse(content={'message':'로그인 성공'},
                        status_code=200)

# 계정 정보 수정
@router.put('/modify_user')
async def modify_user(request:Request):
    
    data = await request.json()
    
    with session_open() as db:
        user = db.query(User).filter(User.user_id == data['user_id']).first()
        
        if new_name := data.get('name'):
            user.name = new_name
        
        if new_role := data.get('role'):
            user.role = new_role
        
        if plain_pw := data.get('password'):
            
            # 비밀번호 유효성 검사
            check_pw_response = check_valid_password(plain_pw)
            if check_pw_response['status_code'] != 200:
                return JSONResponse(content = check_pw_response['content'],
                                    status_code = check_pw_response['status_code'])
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), salt)
            user.password = hashed_pw

        db.commit()
    
    return JSONResponse(content={'message' : '개인정보 수정이 완료되었습니다.'},
                        status_code=200) 


# 아이디 유효성 검사 함수
def check_valid_id(user_id:int):
    
    with session_open() as db:
        
        # DB 내 중복 user_id 검사
        if db.query(User).filter(User.user_id == user_id).count():
            return {'content':{'message' : '중복된 ID입니다.'}, 'status_code':409}
    
    # user_id 유효성 검사
    # user_id는 영문과 숫자를 혼합하여 6자 이상
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    if not bool(re.match(pattern, user_id)):
        return {'content':{'message' : 'ID는 영문자와 숫자를 포함하여 6자 이상입니다.'}, 'status_code' : 409}
    
    return {'content' : {'message' : '사용할 수 있는 ID입니다.'}, 'status_code': 200}


# 비밀번호 유효성 검사 함수
def check_valid_password(password:str):
    
    # 비밀번호는 영문과 숫자를 포함하여 8자 이상
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{8,}$'
    if not bool(re.match(pattern, password)):
        return {'content':{'message' : '비밀번호는 영문자와 숫자를 포함하여 8자 이상입니다.'}, 'status_code' : 409}
    
    return {'content' : {'message' : '사용할 수 있는 비밀번호입니다.'}, 'status_code': 200}



# DB 연결 테스트용
@router.get("/{user_id:int}")
def get_user(user_id:int):
    with session_open() as db:
        user = db.query(User).get(user_id)
    
    return {'result':user}