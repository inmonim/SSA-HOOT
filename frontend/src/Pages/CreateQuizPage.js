import React, { useState, useEffect } from "react";

import axios from "axios";
import CreateQuiz from "../Components/CreateQuiz/CreateQuiz";

function QuizCard({ quiz, answer }) {
  return (
    <div className="card" style={{ border: "solid 1px", marginTop: "5px", width: "400px" }}>
      <p>문제 : {quiz.question}</p>
      <p>미리보기 시간 : {quiz.thumbnail_time}</p>
      <p>풀이 시간 : {quiz.time_limit}</p>
      <div>
        {answer.map(item => (
          <li key={item.answer_num}>{item.answer}</li>
        ))}
      </div>
    </div>
  )
}


function CreateQuizPage() {

  const [quizShow, setQuizShow] = useState('');
  const [quizAnswerPair, setQuizAnswerPair] = useState([]);
  const [lastQuizAnswerPair, setLastQuizAnswerPair] = useState('');

  const [isLoading, setIsLoading] = useState(false);


  const accessToken = localStorage.getItem('accessToken')
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

  useEffect(() => {
    axios.get('http://localhost:8000/create_quiz/get_my_quiz_list?quiz_show_id=1')
      .then(response => {
        console.log(response.data)
        setQuizShow(response.data.quiz_show)
        setQuizAnswerPair(response.data.quiz_answer_pair)

        setLastQuizAnswerPair(response.data.quiz_answer_pair[response.data.quiz_answer_pair.length - 1])
        setIsLoading(true)
      })
      .catch(error => {
        console.log(error)
      })
  }, [])

  return (
    <div>
      <h2>퀴즈쇼 정보</h2>
      <p>{quizShow.quiz_show_name}</p>
      <p>{quizShow.is_open}</p>
      <p>{quizShow.create_date}</p>

      <h2>퀴즈 제작</h2>
      {(isLoading && quizAnswerPair.length) ? <CreateQuiz quizAnswerPair={lastQuizAnswerPair} quizShow={quizShow} /> : <div>생성된 퀴즈가 없습니다!</div>}

      <h2>퀴즈 목록</h2>
      {quizAnswerPair.length ? quizAnswerPair.map(item => (
        <QuizCard
          key={item.in_order}
          quiz={item.quiz}
          answer={item.answer_list}
        />
      )) : <div>생성된 퀴즈가 없습니다!</div>}
    </div>
  )
}


export default CreateQuizPage