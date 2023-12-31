import sys
sys.dont_write_bytecode = True

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user, create_quiz_show, create_quiz

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix='/users', tags=['users'])
app.include_router(create_quiz_show.router, prefix='/create_quiz_show', tags=['create_quiz_show'])
app.include_router(create_quiz.router, prefix='/create_quiz', tags=['create_quiz'])

if __name__ == '__main__':
    import subprocess
    
    subprocess.run(["uvicorn", "main:app", "--reload"])