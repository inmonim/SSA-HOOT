from fastapi import APIRouter


from db_conn import session_open

from models.model import User


router = APIRouter()

# DB 연결 테스트용
@router.get("/{user_id:int}")
def get_user(user_id:int):
    with session_open() as db:
        user = db.query(User).get(user_id)
    
    return {'result':user}