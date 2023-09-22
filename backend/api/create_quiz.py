# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import QuizShow, Quiz

from dto.create_quiz import CreateQuizDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()


@router.post('/creat_quiz')
async def create_quiz(create_quiz_dto : CreateQuizDTO, user: int = Depends(verify_token)):
    
    with session_open() as db:
        quiz_show = db.query(QuizShow).get(create_quiz_dto.quiz_show_id)
        if quiz_show.host_id != user:
            raise HTTPException(detail={'detail':'권한이 없습니다.'}, status_code=403)
        
        quiz = db.query(Quiz)
        
        quiz.quiz_show_id = create_quiz_dto.quiz_show_id
        quiz.question = create_quiz_dto.question
        quiz.question_type = create_quiz_dto.question_type
        quiz.question_img_path = create_quiz_dto.question_img_path
        quiz.thumbnail_time = create_quiz_dto.thumbnail_time
        quiz.time_limit = create_quiz_dto.time_limit
        
        db.add(quiz)
        
        db.commit()
    
    return JSONResponse(content={'detail' : '퀴즈 생성 성공'}, status_code=200)


