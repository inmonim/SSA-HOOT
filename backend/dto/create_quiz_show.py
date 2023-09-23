from pydantic import BaseModel, Field


class CreateQuizShowDTO(BaseModel):
    quiz_show_name : str = Field(..., max_length=20, example="퀴즈 제목")
    description : str = Field(None, max_length=200, example="퀴즈 설명")
    is_open : bool
    
class UpdateQuizShowDTO(BaseModel):
    quiz_show_id : int
    quiz_show_name : str = Field(None, max_length=20, example="퀴즈 제목")
    description : str = Field(None, max_length=200, example="퀴즈 설명")
    is_open : bool = None
    
class QuizSetDTO(BaseModel):
    
    quiz_show_id : int
    quiz_id : int