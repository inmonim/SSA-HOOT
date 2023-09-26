from pydantic import BaseModel
from datetime import datetime


class QuizShowObj(BaseModel):
    id: int
    description: str
    quiz_show_name: str
    is_open: int
    create_date: datetime


class QuizObj(BaseModel):
    id: int
    question: str
    question_type: int
    is_open: int
    question_img_path: str | None
    thumbnail_time: int
    time_limit: int


class AnswerObj(BaseModel):
    id: int
    quiz_id: int
    answer_num: int
    is_answer: int
    answer: str
    answer_img_path: str | None


class QuizAnswerPairObj(BaseModel):
    quiz: QuizObj
    answer_list: list[AnswerObj]
    in_order: int


class QuizListResponse(BaseModel):
    quiz_show: QuizShowObj
    quiz_answer_pair: list[QuizAnswerPairObj]
