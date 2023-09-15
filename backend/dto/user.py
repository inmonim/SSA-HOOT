from pydantic import BaseModel, Field


class CreateUserDTO(BaseModel):
    user_name : str
    user_id : str = Field(..., min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9]{6,}$", description="id는 영문과 숫자를 포함해 6자 이상 20자 이하") 
    password: str = Field(..., min_length=8, max_length=20, pattern=r"^[a-zA-Z0-9\d!@#$%^&*]{8,}$", description="비밀번호는 영문과 숫자를 포함해 8자 이상 20자 이하")
    role : str = "교육생"
    

class LoginDTO(BaseModel):
    user_id : str = Field(..., min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9]{6,}$", description="id는 영문과 숫자를 포함해 6자 이상 20자 이하") 
    password : str = Field(..., min_length=8, max_length=20, pattern=r"^[a-zA-Z0-9\d!@#$%^&*]{8,}$", description="비밀번호는 영문과 숫자를 포함해 8자 이상 20자 이하")


class ModifyeUserDTO(BaseModel):
    user_name : str = None
    user_id : str = Field(..., min_length=6, max_length=20, pattern=r"^[a-zA-Z0-9]{6,}$", description="id는 영문과 숫자를 포함해 6자 이상 20자 이하") 
    password : str = Field(None, min_length=8, max_length=20, pattern=r"^[a-zA-Z0-9\d!@#$%^&*]{8,}$", description="비밀번호는 영문과 숫자를 포함해 8자 이상 20자 이하")
    role : str = None
