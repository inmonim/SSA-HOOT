from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import bcrypt

from db_conn import session_open

from models.model import User


router = APIRouter()

@router.post("/create_user")
async def create_user(request: Request):
    user_data = await request.json()
    
    user_name = user_data['user_name']
    user_id = user_data['user_id']
    plain_pw = user_data['password']
    role = user_data.get('role')
    
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_pw.encode('utf-8'), salt)
    
    with session_open() as db:
        user = User()
        user.student_num = user_id
        user.name = user_name
        user.password = hashed_pw
        user.role = role
        
        db.add(user)
        db.commit()
    
    return JSONResponse(content={''})


# DB 연결 테스트용
@router.get("/{user_id:int}")
def get_user(user_id:int):
    with session_open() as db:
        user = db.query(User).get(user_id)
    
    return {'result':user}