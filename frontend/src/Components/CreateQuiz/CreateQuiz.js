import axios from "axios";
import React, { useEffect, useState } from "react";

import CreateQuizAnswer from "./CreateQuizAnswer";

function CreateQuiz({ quizAnswerPair, quizShow }) {
  const [question, setQuestion] = useState('');
  const [questionType, setQuestionType] = useState('');
  const [questionImgPath, setQuestionImgPath] = useState('');
  const [thumbnailTime, setThumbnailTime] = useState('');
  const [timeLimit, setTimeLimit] = useState('');
  const [isOpen, setIsOpen] = useState('');

  const [answerList, setAnswerList] = useState([]);

  const accessToken = localStorage.getItem('accessToken')
  axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

  const timeOption = [5, 10, 15, 20, 30, 60, 120, 300, 1200]
  const questionTypeOption = ["설명", "선택형", "OX", "단어 맞추기", "초성 퀴즈"]

  useEffect(() => {
    const quiz = quizAnswerPair.quiz

    setAnswerList(quizAnswerPair.answer_list)

    setQuestion(quiz.question)
    setQuestionType(quiz.question_type)
    setQuestionImgPath(quiz.question_img_path)
    setThumbnailTime(quiz.thumbnail_time)
    setTimeLimit(quiz.time_limit)
    setIsOpen(quiz.is_open)
  }, [])

  const addQuiz = () => {
    setAnswerList((answerList) => [...answerList, null])
  }

  // useEffect(() => {
  //   console.log(isOpen)
  // }, [isOpen])

  const quizData = {
    quiz_show_id: quizShow.id
  }

  // changeQuiz(() => {
  //   axios.post("http://localhost:8000/create_quiz/create_quiz",).
  // })


  return (
    <div className="card" style={{ border: "solid 1px", marginTop: "5px", width: "400px" }}>

      <div>
        <label>퀴즈 형식</label>
        <select
          value={questionTypeOption[questionType]}
          onChange={(e) => setQuestionType(e.target.value)}
        >
          {questionTypeOption.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label>퀴즈 본문</label>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
      </div>
      <div>
        <label> 퀴즈 제한 시간 </label>
        <select
          value={timeLimit}
          onChange={(e) => setTimeLimit(e.target.value)}
        >
          {timeOption.map((time) => (
            <option key={time} value={time}>
              {time} 분
            </option>
          ))}
        </select>
      </div>
      <div>
        <label> 미리보기 시간 </label>
        <input
          value={thumbnailTime}
          type="number"
          onChange={(e) => setThumbnailTime(e.target.value)}
        />
      </div>
      <div>
        <input
          type="checkbox"
          value={isOpen ? true : false}
          onChange={(e) => setIsOpen(e.target.checked)}
        />
      </div>
      <div>
        <button
        // onClick={}
        >

        </button>
      </div>
      <div>
        {answerList.map((answer) => (
          <CreateQuizAnswer answerObj={answer} />
        ))}
        <button
          onClick={addQuiz}
        >+</button>
      </div>
    </div>
  )
}

export default CreateQuiz