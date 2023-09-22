# FastAPI
from fastapi import APIRouter, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import QuizShow

from dto.create_quiz_show import CreateQuizShowDTO, UpdateQuizShowDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()

@router.post('/create_quiz_show')
async def create_quiz_show(request_data : CreateQuizShowDTO, user : int =  Depends(verify_token)):
    
    quiz_name = request_data.quiz_name
    description = request_data.description
    is_open = request_data.is_open
    
    with session_open() as db:
        
        quiz_show = QuizShow()
        quiz_show.quiz_name = quiz_name
        quiz_show.host_id = user
        quiz_show.description = description
        quiz_show.is_open = is_open
        
        db.add(quiz_show)
        db.commit()
    
    return JSONResponse(content={"detail" : "퀴즈 생성 완료"}, status_code=200)


@router.put('/update_quiz_show')
async def update_quiz_show(request_data : UpdateQuizShowDTO, user : int =  Depends(verify_token)):
    
    quiz_id = request_data.quiz_id
    quiz_name = request_data.quiz_name
    description = request_data.description
    is_open = request_data.is_open 
    
    with session_open() as db:
        
        quiz_show = db.query(QuizShow).get(quiz_id)
        
        if quiz_show.host_id != user:
            raise HTTPException(detail={"detail" : "권한이 없습니다."}, status_code=403)
        
        if quiz_name:
            quiz_show.quiz_name = quiz_name
        if description:
            quiz_show.description = description
        if is_open:
            quiz_show.is_open = is_open
        
        db.commit()
    
    return JSONResponse(content={"detail":"수정 완료"}, status_code=200)

@router.delete('/delete_quiz_show')
async def delete_quiz_show(quiz_id:int, user : int =  Depends(verify_token)):
    
    with session_open() as db:
        quiz_show = db.query(QuizShow).get(quiz_id)
        
        if quiz_show.host_id != user:
            raise HTTPException(content={"detail":"권한이 없습니다."}, status_code=403)
        
        db.delete(quiz_show)
        
        db.commit()
    
    return JSONResponse(content={"detail":"삭제 완료"}, status_code=200)