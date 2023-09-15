# FastAPI
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

# 모듈 및 패키지
import bcrypt
import re

# DB
from db_conn import session_open

# model, DTO
from models.model import User
from dto.user import ( CreateUserDTO, LoginDTO, ModifyeUserDTO )

# router 등록
router = APIRouter()

# 계정 생성 요청
@router.post("/create_user")
async def create_user(create_user_data: CreateUserDTO):
    
    user_name = create_user_data.user_name
    user_id = create_user_data.user_id
    plain_pw = create_user_data.password
    role = create_user_data.role
    
    # user_id 재검사
    check_id_response = check_valid_id(user_id)
    if check_id_response['status_code'] != 200:
        raise HTTPException(detail=check_id_response['detail'],
                             status_code=check_id_response['status_code'])
        
    # 비밀번호 유효성 재검사
    check_pw_response = check_valid_password(plain_pw)
    if check_pw_response['status_code'] != 200:
        raise HTTPException(detail=check_pw_response['detail'],
                             status_code=check_pw_response['status_code'])
    
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
    
    return JSONResponse(content = {'detail':'계정이 생성되었습니다.'},
                        status_code = 200)

# 아이디 유효성 검사 요청
@router.post('/create_user/check_valid_id')
async def check_valid_id_request(request:Request):
    
    data = await request.json()
    
    user_id = data['user_id']
    
    check_id_response = check_valid_id(user_id)
    if check_id_response['status_code'] != 200:
        raise HTTPException(detail=check_id_response['detail'],
                             status_code=check_id_response['status_code'])
    
    return JSONResponse(content={'detail':check_id_response['detail']},
                        status_code=check_id_response['status_code'])

# 로그인 요청
@router.post('/login')
async def login(request_data: LoginDTO):
    
    input_id = request_data.user_id
    input_pw = request_data.password
    
    with session_open() as db:
        
        user = db.query(User).filter(User.user_id == input_id).first()
        
        # user_id가 DB에 없을 경우
        if not user:
            raise HTTPException(detail = '존재하지 않는 계정입니다.',
                                status_code=401)
        
        # user_id로 DB에서 가져온 비밀번호 정보
        hashed_pw = user.password
        
        # 비밀번호가 없을 경우
        if bcrypt.checkpw(input_pw.encode('utf-8'), hashed_pw.encode('utf-8')) == False:
            raise HTTPException(detail = '비밀번호가 틀렸습니다.',
                                status_code=401)
    
    return JSONResponse(content={'detail':'로그인 성공'},
                        status_code=200)

# 계정 정보 수정
@router.put('/modify_user')
def modify_user(request_data:ModifyeUserDTO):
    
    user_id = request_data.user_id
    new_name = request_data.user_name
    new_plain_pw = request_data.password
    new_role = request_data.role
    
    with session_open() as db:
        user = db.query(User).filter(User.user_id == user_id).first()
        
        if new_name:
            user.name = new_name
        
        if new_role:
            user.role = new_role
        
        if new_plain_pw:
            
            # 비밀번호 유효성 검사
            check_pw_response = check_valid_password(new_plain_pw)
            if check_pw_response['status_code'] != 200:
                raise JSONResponse(content = check_pw_response['detail'],
                                    status_code = check_pw_response['status_code'])
                
            # 유효성 검사 통과 시 비밀번호 재생성
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(new_plain_pw.encode('utf-8'), salt)
            user.password = hashed_pw

        db.commit()
    
    return JSONResponse(content={'detail' : '개인정보 수정이 완료되었습니다.'},
                        status_code=200) 


# 아이디 유효성 검사 함수
def check_valid_id(user_id:int):
    
    with session_open() as db:
        
        # DB 내 중복 user_id 검사
        if db.query(User).filter(User.user_id == user_id).count():
            return {'detail': '중복된 ID입니다.', 'status_code':409}
    
    # user_id 유효성 검사
    # user_id는 영문과 숫자를 혼합하여 6자 이상
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'
    if not bool(re.match(pattern, user_id)):
        return {'detail' : 'ID는 영문자와 숫자를 포함하여 6자 이상입니다.', 'status_code' : 409}
    
    return {'detail': '사용할 수 있는 ID입니다.', 'status_code': 200}


# 비밀번호 유효성 검사 함수
def check_valid_password(password:str):
    
    # 비밀번호는 영문과 숫자를 포함하여 8자 이상
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).{8,}$'
    if not bool(re.match(pattern, password)):
        return {'detail' : '비밀번호는 영문자와 숫자를 포함하여 8자 이상입니다.', 'status_code' : 409}
    
    return {'detail' : '사용할 수 있는 비밀번호입니다.', 'status_code': 200}