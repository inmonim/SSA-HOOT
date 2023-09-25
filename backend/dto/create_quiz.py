from pydantic import BaseModel, Field


# 퀴즈 클래스
class Quiz(BaseModel):
    quiz_id: int = None
    question: str = Field(..., max_length=300, example="SSA-HOOT의 개발자는?")
    question_type: int = Field(
        ...,
        le=20,
        ge=1,
        description="1: 다지선다\n2: 참거짓\n3:초성 퀴즈\n4:단어맞추기\n5:배열 맞추기",
        example=1,
    )
    question_img_path: str = None
    thumbnail_time: int = Field(5, le=30, ge=0, example=5)
    time_limit: int = Field(20, le=120, ge=5)
    is_open: int = Field(1, le=10, ge=0, example=1)


# 퀴즈의 답변 항목 클래스
class Answer(BaseModel):
    answer_id: int = None
    quiz_id: int = None
    answer_num: int = Field(..., le=10, ge=1, example=1)
    answer: str = Field(..., max_length=100, example="답변")
    is_answer: int = Field(..., le=10, ge=1, example=1)
    answer_img_path: str = None


# 퀴즈 - 답변
class QuizAnswerPair(BaseModel):
    quiz: Quiz
    answer: list[Answer] = None


# 퀴즈 생성용 DTO
class CreateQuizDTO(BaseModel):
    quiz_show_id: int
    in_order: int = Field(None, description="퀴즈쇼 - 퀴즈 연결 테이블에서 순서를 타나냄")
    quiz_answer_pair: QuizAnswerPair


# 퀴즈 순서쌍
class QuizOrderPair(BaseModel):
    quiz_id: int
    in_order: int


# 퀴즈 순서 업데이트용 DTO
class UpdateQuizOrderDTO(BaseModel):
    quiz_show_id: int
    quiz_order_pair: list[QuizOrderPair]


class UpdateQuizDTO(BaseModel):
    question: str = Field(None, max_length=300)
    question_type: int = Field(
        None,
        le=20,
        ge=1,
        description="1: 다지선다\n2: 참거짓\n3:초성 퀴즈\n4:단어맞추기\n5:배열 맞추기",
        example=1,
    )
    question_img_path: str = None
    thumbnail_time: int = Field(None, le=30, ge=0, example=5)
    time_limit: int = Field(None, le=120, ge=5)
    is_open: int = Field(1, le=10, ge=0)


class QuizID(BaseModel):
    quiz_id: int
