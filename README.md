
23/09/13

- 회원가입, 비밀번호 암호화, 로그인 API 구현

- 다만 유지보수와 가독성 향상을 위해 Pydantic 모델을 활용하여 DTO 방식을 구현할 예정

23/09/14

- Pydantic 모델 활용 이외의 방법을 생각했으나, Pydantic이 가장 붙임성이 좋은 것 같음

23/09/15

- Pydantic을 통한 User 단위의 DTO 구현

- JWT 구현 예정

23/09/18

- 비밀번호 암호화는 bcypt 라이브러리 활용 (salting + hashing)