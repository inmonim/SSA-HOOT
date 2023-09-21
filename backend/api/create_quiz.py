# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import QuizShow

from dto.create_quiz import CreateQuizDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()

@router.post('/creat_quiz')
async def create_quiz(reqeust_data : CreateQuizDTO, token: str = Header(None)):
    pass