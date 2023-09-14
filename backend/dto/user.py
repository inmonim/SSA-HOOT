from pydantic import BaseModel, constr

class CreateUser(BaseModel):
    user_name : str
    user_id : str
    password: str
    role : str