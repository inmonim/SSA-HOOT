from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml


# config.yaml 파일의 db 연결 정보 불러오기
with open('./config.yaml', 'r') as cf:
    db = yaml.safe_load(cf)

# config.yaml 내의 db map 데이터를 통해 db 연결 정보 채우기
username = db['db']['username']
host = db['db']['host']
port = db['db']['port']
password = db['db']['password']
database = db['db']['database']

db_url = f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'

# 엔진 객체 생성
engine = create_engine(db_url)

# 세션메이커 객체 생성
session_open = sessionmaker(bind=engine)