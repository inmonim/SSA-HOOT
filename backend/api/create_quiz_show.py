# FastAPI
from fastapi import APIRouter, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, Rseponse, JWT
from models.model import QuizShow, QuizShow_Quiz, Quiz

from dto.create_quiz_show import CreateQuizShowDTO, UpdateQuizShowDTO, QuizSetDTO

from response.create_quiz_show import QuizShowListResponse, QuizShowResponse

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()


# 퀴즈쇼 생성
@router.post("/create_quiz_show")
async def create_quiz_show(
    create_quiz_show_dto: CreateQuizShowDTO, user: int = Depends(verify_token)
):
    quiz_show_name = create_quiz_show_dto.quiz_show_name
    description = create_quiz_show_dto.description
    is_open = create_quiz_show_dto.is_open

    with session_open() as db:
        quiz_show = QuizShow()
        quiz_show.quiz_show_name = quiz_show_name
        quiz_show.host_id = user
        quiz_show.description = description
        quiz_show.is_open = is_open

        db.add(quiz_show)
        db.commit()

    return JSONResponse(content={"detail": "퀴즈 생성 완료"}, status_code=200)


# 퀴즈쇼 업데이트
@router.put("/update_quiz_show")
async def update_quiz_show(
    update_quiz_show_dto: UpdateQuizShowDTO, user: int = Depends(verify_token)
):
    quiz_show_id = update_quiz_show_dto.quiz_show_id
    quiz_show_name = update_quiz_show_dto.quiz_show_name
    description = update_quiz_show_dto.description
    is_open = update_quiz_show_dto.is_open

    with session_open() as db:
        quiz_show = db.query(QuizShow).get(quiz_show_id)

        if quiz_show.host_id != user:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)

        if quiz_show_name:
            quiz_show.quiz_show_name = quiz_show_name
        if description:
            quiz_show.description = description
        if is_open:
            quiz_show.is_open = is_open

        db.commit()

    return JSONResponse(content={"detail": "수정 완료"}, status_code=200)


# 퀴즈쇼 삭제
@router.delete("/delete_quiz_show")
async def delete_quiz_show(quiz_id: int, user: int = Depends(verify_token)):
    with session_open() as db:
        quiz_show = db.query(QuizShow).get(quiz_id)
        if not quiz_show:
            raise HTTPException(detail="존재하지 않는 리소스입니다.", status_code=410)

        if quiz_show.host_id != user:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)

        db.delete(quiz_show)

        db.commit()

    return JSONResponse(content={"detail": "삭제 완료"}, status_code=200)


# 나의 퀴즈쇼 리스트 확인
@router.get("/get_my_quiz_show_list", response_model=QuizShowListResponse)
async def get_my_quiz_show_list(user: int = Depends(verify_token)):
    with session_open() as db:
        quiz_show_list = db.query(QuizShow).filter(QuizShow.host_id == user).all()

    result = {"quiz_show_list": quiz_show_list}

    return result
