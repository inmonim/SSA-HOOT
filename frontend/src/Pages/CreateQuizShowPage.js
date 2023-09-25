import axios from "axios";

import React, { useEffect, useState } from "react";


function CreateQuizShowPage() {
  const [quizShowName, setQuizShowName] = useState('');
  const [description, setDescription] = useState('');
  const [isOpen, setIsOpen] = useState(true);

  const createQuizShow = () => {

    const quizShowData = {
      quiz_show_name: quizShowName,
      description: description,
      is_open: isOpen
    }

    const accessToken = localStorage.getItem('accessToken')
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;

    axios.post('http://localhost:8000/create_quiz_show/create_quiz_show', quizShowData)
      .then(response => {
        console.log(response)
      })
      .catch(error => {
        console.log(error)
      })
  }

  return (
    <div>
      <h1>퀴즈쇼 생성!</h1>

      <input
        type="text"
        value={quizShowName}
        placeholder="퀴즈쇼 제목"
        onChange={(e) => setQuizShowName(e.target.value)}
      />
      <input
        type="text"
        value={description}
        placeholder="퀴즈쇼 설명"
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        type="checkbox"
        value={isOpen}
        onChange={(e) => setIsOpen(e.target.value)}
      />
      <button onClick={createQuizShow}>퀴즈쇼 생성</button>
    </div>
  )
}


export default CreateQuizShowPage