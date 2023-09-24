from sqlalchemy.ext.automap import automap_base
from db_conn import engine

# 베이스 모델 생성
Base = automap_base()

# DB 엔진 연결
Base.prepare(engine)

# 모델 미러링
User = Base.classes.user
QuizShow = Base.classes.quiz_show
Quiz = Base.classes.quiz
QuizAnswer = Base.classes.quiz_answer

# QuizShow - Quiz 연결 테이블
QuizShow_Quiz = Base.classes.quiz_show_quiz








Test = Base.classes.test