# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import QuizShow, QuizShow_Quiz, Quiz, QuizAnswer

from dto.create_quiz import CreateQuizDTO, UpdateQuizOrderDTO, QuizID

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()


# 퀴즈와 답변 쌍은 무조건 그 편집화면을 나가기 전에 저장해야함.
@router.post("/create_quiz")
async def create_quiz(
    create_quiz_dto: CreateQuizDTO, user: int = Depends(verify_token)
):
    # 퀴즈와 연결된 퀴즈쇼 ID 및, 퀴즈쇼 내 퀴즈의 순서
    quiz_show_id = create_quiz_dto.quiz_show_id
    in_order = create_quiz_dto.in_order

    # (퀴즈 - 답변 리스트)
    quiz_answer_pair = create_quiz_dto.quiz_answer_pair

    # 퀴즈
    quiz_data = quiz_answer_pair.quiz

    # 순서로 정렬한 답변 목록
    answer_list = sorted(quiz_answer_pair.answer, key=lambda x: x.answer_num)

    with session_open() as db:
        # 다른 유저의 접근 차단
        quiz_show = db.query(QuizShow).get(quiz_show_id)
        if quiz_show.host_id != user:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)

        # 퀴즈와 답변 쌍을 새로 만드는 경우
        if not quiz_data.quiz_id:
            quiz = Quiz()
            quiz.user_id = user
            quiz.question = quiz_data.question
            quiz.question_type = quiz_data.question_type
            quiz.question_img_path = quiz_data.question_img_path
            quiz.thumbnail_time = quiz_data.thumbnail_time
            quiz.time_limit = quiz_data.time_limit
            quiz.is_open = quiz_data.is_open

            db.add(quiz)
            # quiz 객체의 id 생성을 위해 commit
            db.commit()

            # 답변 쌍도 새롭게 생성
            for answer_data in answer_list:
                answer = QuizAnswer()
                answer.quiz_id = quiz.id
                answer.answer_num = answer_data.answer_num
                answer.answer = answer_data.answer
                answer.is_answer = answer_data.is_answer
                answer.answer_img_path = answer_data.answer_img_path

                db.add(answer)

        # 이미 존재하는 퀴즈를 수정하는 경우
        else:
            # 기존의 퀴즈 객체 가져오기
            quiz = db.query(Quiz).get(quiz_data.quiz_id)
            quiz.user_id = user
            quiz.question = quiz_data.question
            quiz.question_type = quiz_data.question_type
            quiz.question_img_path = quiz_data.question_img_path
            quiz.thumbnail_time = quiz_data.thumbnail_time
            quiz.time_limit = quiz_data.time_limit
            quiz.is_open = quiz_data.is_open

            # 존재하던 퀴즈 답변 쌍 받아온 뒤, answer_num 기준으로 정렬
            old_answer_list = (
                db.query(QuizAnswer).filter(QuizAnswer.quiz_id == quiz.id).all()
            )
            old_answer_list.sort(key=lambda x: x.answer_num)

            # 존재하던 답변에 answer_num 순서로 덮어씌우기
            for i in range(len(answer_list)):
                new_answer = answer_list[i]

                # 존재하던 답변의 개수가 생성할 퀴즈의 수보다 작아진 경우
                if len(old_answer_list) <= i:
                    answer = QuizAnswer()

                # 생성할 퀴즈의 수가 존재하던 답변의 수와 같거나 작기 전까지
                else:
                    answer = old_answer_list[i]

                answer.quiz_id = quiz.id
                answer.answer_num = new_answer.answer_num
                answer.answer = new_answer.answer
                answer.is_answer = new_answer.is_answer
                answer.answer_img_path = new_answer.answer_img_path

                db.add(answer)

            # 새로운 답변보다 많았던 기존의 답변 삭제
            for i in range(len(answer_list), len(old_answer_list)):
                old_answer = old_answer_list[i]

                db.delete(old_answer)

        # 퀴즈쇼 - 퀴즈에서 순서를 조정
        # quiz_show_id 및 quiz_id 연결쌍이 존재하는 경우, 순서만 수정
        # 다만, 퀴즈 생성에서 순서를 자유롭게 할 게 아니라면, 아래 코드는 불필요할 수 있음.
        if (
            quiz_show_quiz := db.query(QuizShow_Quiz)
            .filter(
                QuizShow_Quiz.quiz_show_id == quiz_show_id,
                QuizShow_Quiz.quiz_id == quiz.id,
            )
            .first()
        ):
            quiz_show_quiz.in_order = in_order

        # quiz_show_id - quiz_id 연결쌍이 없는 경우 신규 생성
        else:
            quiz_show_quiz = QuizShow_Quiz()
            quiz_show_quiz.quiz_show_id = quiz_show_id
            quiz_show_quiz.quiz_id = quiz.id
            quiz_show_quiz.in_order = in_order

        db.add(quiz_show_quiz)

        db.commit()

    return JSONResponse(content={"detail": "데이터 입력 성공"}, status_code=200)


# 퀴즈쇼 내의 퀴즈 순서 수정
@router.post("/change_order")
async def change_quiz_order(quiz_order_dto: UpdateQuizOrderDTO, user: int = Depends(verify_token)):
    quiz_show_id = quiz_order_dto.quiz_show_id

    # 새로운 퀴즈쇼 - 퀴즈 순서 데이터 불러와 순서대로 정렬
    quiz_order_pair_list = quiz_order_dto.quiz_order_pair
    quiz_order_pair_list.sort(key=lambda x: x.quiz_id)

    with session_open() as db:
        # 악의적 접근 차단
        quiz_show = db.query(QuizShow).get(quiz_show_id)
        if quiz_show.host_id != user:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)

        # 이전 퀴즈쇼-퀴즈 연결 테이블 값 불러와 순서대로 정렬
        order_list = (
            db.query(QuizShow_Quiz)
            .filter(QuizShow_Quiz.quiz_show_id == quiz_show_id)
            .all()
        )
        order_list.sort(key=lambda x: x.quiz_id)

        # 정렬할 퀴즈의 길이가 맞지 않을 경우(있을지 모르겠으나)
        if not (len(order_list) is len(quiz_order_pair_list)):
            raise HTTPException(detail="퀴즈의 개수가 맞지 않습니다.", status_code=409)

        for i in range(len(order_list)):
            new_order = order_list[i]
            new_order.in_order = quiz_order_pair_list[i].in_order

            db.add(new_order)

        db.commit()

    return JSONResponse(content={"detail": "순서 변환 성공"}, status_code=200)


# 퀴즈 삭제
@router.delete("/delete_quiz")
async def delete_quiz(quiz_id: QuizID, user: int = Depends(verify_token)):
    quiz_id = quiz_id.quiz_id
    with session_open() as db:
        quiz = db.query(Quiz).get(quiz_id)
        if quiz.user_id != user:
            raise HTTPException(detail="권한이 없습니다", status_code=403)

        answer_list = db.query(QuizAnswer).filter(QuizAnswer.quiz_id == quiz_id).all()
        for answer in answer_list:
            db.delete(answer)
        
        # 퀴즈쇼 - 퀴즈 연결 테이블에서 퀴즈 삭제
        quiz_show_quiz = db.query(QuizShow_Quiz).filter(QuizShow_Quiz.quiz_id == quiz_id).first()
        quiz_show_id = quiz_show_quiz.quiz_show_id
        
        # 삭제될 퀴즈의 순서 파악
        quiz_in_order = quiz_show_quiz.in_order
        
        # 삭제될 퀴즈가 속한 퀴즈쇼 내에서, 해당 퀴즈보다 후순위에 있는 퀴즈 객체 가져오기
        quiz_show_quiz_list = db.query(QuizShow_Quiz).filter(QuizShow_Quiz.quiz_show_id == quiz_show_id, QuizShow_Quiz.in_order > quiz_in_order).all()
        
        # 퀴즈의 순서 한 칸 씩 당기기
        for qsq in quiz_show_quiz_list:
            qsq.in_order -= 1
            db.add(qsq)
        
        # 퀴즈쇼 - 퀴즈 객체 삭제
        db.delete(quiz_show_quiz)
        
        # 퀴즈 삭제
        db.delete(quiz)
        db.commit()

    return JSONResponse(content={"detail": "퀴즈 삭제 완료"}, status_code=200)


# open된 quiz를 user가 가져오기
@router.post("/get_open_quiz")
async def get_open_quiz(quiz_id: int, user: int = Depends(verify_token)):
    with session_open() as db:
        quiz = db.query(Quiz).get(quiz_id)

        # 퀴즈가 존재하는지 확인
        if not quiz:
            raise HTTPException(detail="존재하지 않는 컨텐츠입니다.", status_code=404)

        # 오픈되어있는 퀴즈인지 확인
        if quiz.is_open == 0:
            raise HTTPException(detail="권한이 없습니다.", status_code=403)

        # 새로운 퀴즈 객체로 할당, user_id만 변경
        clone_quiz = Quiz()
        clone_quiz.user_id = user
        clone_quiz.question = quiz.question
        clone_quiz.question_type = quiz.question_type
        clone_quiz.question_img_path = quiz.question_img_path
        clone_quiz.thumbnail_time = quiz.thumbnail_time
        clone_quiz.time_limit = quiz.time_limit

        # 새로운 퀴즈 객체 등록
        db.add(clone_quiz)
        db.commit()

    return JSONResponse(content={"detail": "퀴즈 가져오기 성공"}, status_code=200)
