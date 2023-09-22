# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import QuizShow, QuizShow_Quiz, Quiz

from dto.create_quiz import CreateQuizDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()

# 퀴즈 생성
@router.post('/creat_quiz')
async def create_quiz(create_quiz_dto : CreateQuizDTO, user: int = Depends(verify_token)):
    
    with session_open() as db:
        
        quiz = Quiz()

        quiz.question = create_quiz_dto.question
        quiz.question_type = create_quiz_dto.question_type
        quiz.question_img_path = create_quiz_dto.question_img_path
        quiz.thumbnail_time = create_quiz_dto.thumbnail_time
        quiz.time_limit = create_quiz_dto.time_limit

        db.add(quiz)
        db.commit()
        
        # quiz_show에서 생성하여 quiz_show_id가 입력된 경우, 자동으로 연결테이블 값 추가
        quiz_show_id = create_quiz_dto.quiz_show_id
        
        if quiz_show_id:
            quiz_show = db.query(QuizShow).get(quiz_show_id)
            
            # 다른 유저의 악의적 접근 차단
            if quiz_show.host_id != user:
                raise HTTPException(detail={'detail':'권한이 없습니다.'}, status_code=403)
            
            quiz_show_quiz = QuizShow_Quiz()
            quiz_show_quiz.quiz_show_id = quiz_show_id
            quiz_show_quiz.quiz_id = quiz.id
            
            db.add(quiz)
            db.commit()
        
        # 퀴즈와 이를 사용하는 유저의 관계 테이블 만들어야 함.
        
    return JSONResponse(content={'detail' : '퀴즈 생성 성공'}, status_code=200)


# 퀴즈