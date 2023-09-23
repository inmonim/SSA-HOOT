# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import ( QuizShow, QuizShow_Quiz, Quiz, User_Quiz )

from dto.create_quiz import CreateQuizDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()

# 퀴즈 생성
@router.post('/creat_quiz')
async def create_quiz(create_quiz_dto : CreateQuizDTO, user: int = Depends(verify_token)):
    
    with session_open() as db:
        
        quiz = Quiz()

        # 기본적인 퀴즈 객체 생성
        quiz.question = create_quiz_dto.question
        quiz.question_type = create_quiz_dto.question_type
        quiz.question_img_path = create_quiz_dto.question_img_path
        quiz.thumbnail_time = create_quiz_dto.thumbnail_time
        quiz.time_limit = create_quiz_dto.time_limit
        quiz.is_open = create_quiz_dto.is_open

        db.add(quiz)
        db.commit()
        
        # quiz_show에서 생성하여 quiz_show_id가 입력된 경우, 자동으로 연결테이블 값 추가
        quiz_show_id = create_quiz_dto.quiz_show_id
        
        if quiz_show_id:
            quiz_show = db.query(QuizShow).get(quiz_show_id)
            
            # 다른 유저의 악의적 접근 차단
            if quiz_show.host_id != user:
                raise HTTPException(detail='권한이 없습니다.', status_code=403)
            
            quiz_show_quiz = QuizShow_Quiz()
            quiz_show_quiz.quiz_show_id = quiz_show_id
            quiz_show_quiz.quiz_id = quiz.id
            
            db.add(quiz_show_quiz)
        
        # 해당 퀴즈의 주인인 User와의 연결 테이블 생성
        user_quiz = User_Quiz()
        user_quiz.user_id = user
        user_quiz.quiz_id = quiz.id
        db.add(user_quiz)
            
        db.commit()
        
    return JSONResponse(content={'detail' : '퀴즈 생성 성공'}, status_code=200)

# open된 quiz를 user가 가져오기
@router.post('/get_open_quiz')
async def get_open_quiz(quiz_id : int, user: int = Depends(verify_token)):
    
    with session_open() as db:
        
        quiz = db.query(Quiz).get(quiz_id)
        
        # 퀴즈가 존재하는지 확인
        if not quiz:
            raise HTTPException(detail="존재하지 않는 컨텐츠입니다.", status_code=404)

        # 오픈되어있는 퀴즈인지 확인
        if quiz.is_open == 0:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)
        
        # 중복으로 가지고 있는지 확인
        if db.query(User_Quiz).filter(User_Quiz.user_id==user, User_Quiz.quiz_id==quiz_id).first():
            raise HTTPException(detail="이미 존재하는 컨텐츠입니다.", status_code=409)

        user_quiz = User_Quiz()
        user_quiz.user_id = user
        user_quiz.quiz_id = quiz_id
        
        db.add(user_quiz)
        db.commit()
        
    return JSONResponse(content={'detail' : "퀴즈 가져오기 성공"}, status_code=200)