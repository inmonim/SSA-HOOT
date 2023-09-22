from pydantic import BaseModel, Field


class CreateQuizDTO(BaseModel):
    
    quiz_show_id : int = None
    question : str = Field(..., max_length=300, example="SSA-HOOT의 개발자는?")
    question_type : int = Field(..., le=20, ge=1,
                                description="1: 다지선다\n2: 참거짓\n3:초성 퀴즈\n4:단어맞추기\n5:배열 맞추기",
                                example=1)
    question_img_path : str = None
    thumbnail_time : int = Field(5,le=30, ge=0, example=5)
    time_limit : int = Field(20, le=120, ge=0)