import sys
sys.dont_write_bytecode = True

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from api import user, create_quiz_show

app = FastAPI()

origins = [""]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(user.router, prefix='/users', tags=['users'])
app.include_router(create_quiz_show.router, prefix='/create_quiz_show', tags=['create_quiz_show'])

if __name__ == '__main__':
    import subprocess
    
    subprocess.run(["uvicorn", "main:app", "--reload"])