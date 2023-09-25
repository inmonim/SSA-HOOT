from pydantic import BaseModel
from datetime import datetime


class QuizShowResponse(BaseModel):
    id: int
    description: str
    quiz_show_name: str
    is_open: int
    create_date: datetime


class QuizShowListResponse(BaseModel):
    quiz_show_list: list[QuizShowResponse]
