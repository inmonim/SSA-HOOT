# FastAPI
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse

# 모듈 및 패키지

# DB
from db_conn import session_open

# model, DTO, JWT
from models.model import ( QuizShow, QuizShow_Quiz, Quiz, QuizAnswer )

from dto.create_quiz import CreateQuizDTO

from auth.jwt_module import verify_token

# router 등록
router = APIRouter()

# 퀴즈와 답변 쌍은 무조건 그 편집화면을 나가기 전에 저장해야함.
@router.post('/test')
async def test(create_quiz_dto: CreateQuizDTO, user : int = Depends(verify_token)):
    quiz_show_id = create_quiz_dto.quiz_show_id
    in_order = create_quiz_dto.in_order
    
    quiz_answer_pair = create_quiz_dto.quiz_answer_pair
    quiz_data = quiz_answer_pair.quiz
    answer_list = sorted(quiz_answer_pair.answer, key=lambda x:x.answer_num)
    
    with session_open() as db:
        
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
            db.commit()
            
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
            quiz = db.query(Quiz).get(quiz_data.quiz_id)
            quiz.user_id = user
            quiz.question = quiz_data.question
            quiz.question_type = quiz_data.question_type
            quiz.question_img_path = quiz_data.question_img_path
            quiz.thumbnail_time = quiz_data.thumbnail_time
            quiz.time_limit = quiz_data.time_limit
            quiz.is_open = quiz_data.is_open
            
            
            # 존재하던 퀴즈 답변 쌍 받아온 뒤, answer_num 기준으로 정렬
            old_answer_list = db.query(QuizAnswer).filter(QuizAnswer.quiz_id==quiz.id).all()
            old_answer_list.sort(key=lambda x:x.answer_num)
            
            
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
        if quiz_show_quiz := db.query(QuizShow_Quiz).filter(QuizShow_Quiz.quiz_show_id == quiz_show_id, QuizShow_Quiz.quiz_id==quiz.id).first():
            quiz_show_quiz.in_order = in_order
        else:
            quiz_show_quiz = QuizShow_Quiz()
            quiz_show_quiz.quiz_show_id = quiz_show_id
            quiz_show_quiz.quiz_id = quiz.id
            quiz_show_quiz.in_order = in_order
            
        db.add(quiz_show_quiz)
          
        db.commit()
    
    return JSONResponse(content={"detail" : "데이터 입력 성공"}, status_code=200)

# 퀴즈 생성
@router.post('/creat_quiz')
async def create_quiz(create_quiz_dto : CreateQuizDTO, user: int = Depends(verify_token)):
    
    
    with session_open() as db:
        
        quiz = Quiz()

        # 기본적인 퀴즈 객체 생성
        quiz.user_id = user
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
            
            in_order = create_quiz_dto.in_order
            
            quiz_show_quiz = QuizShow_Quiz()
            quiz_show_quiz.quiz_show_id = quiz_show_id
            quiz_show_quiz.quiz_id = quiz.id
            quiz_show_quiz.in_order = in_order
            
            db.add(quiz_show_quiz)
            
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
        
    return JSONResponse(content={'detail' : "퀴즈 가져오기 성공"}, status_code=200)


@router.post('/')
async def testtttest():
    with session_open() as db:
        
        quiz_answer = db.query(QuizAnswer).get(1)
        
        quiz_answer.answer = "이것은 바뀌는지 테스트 해볼라고!"
        
        db.add(quiz_answer)
        db.commit()
        

        
    return JSONResponse(content=quiz_answer)