from pydantic import BaseModel, Field


class CreateQuizShowDTO(BaseModel):
    quiz_name : str = Field(..., max_length=20, example="퀴즈 제목")
    description : str = Field(None, max_length=200, example="퀴즈 설명")
    is_open : bool
    
class UpdateQuizShowDTO(BaseModel):
    quiz_id : int
    quiz_name : str = Field(None, max_length=20, example="퀴즈 제목")
    description : str = Field(None, max_length=200, example="퀴즈 설명")
    is_open : bool = None