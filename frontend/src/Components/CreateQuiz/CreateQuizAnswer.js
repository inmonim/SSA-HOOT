import React, { useEffect, useState } from "react";

function CreateQuizAnswer({ answerItem }) {

  const [answerId, setAnswerId] = useState('');
  const [quizId, setQuizId] = useState('');
  const [answerNum, setAnswerNum] = useState('');
  const [isAnswer, setIsAnswer] = useState(false);
  const [answer, setAnswer] = useState('');
  const [answerImgPath, setAnswerImgPath] = useState('');

  useEffect(() => {

    const answerObj = answerItem

    if (answerObj.id) {
      setAnswerId(answerObj.id)
      setQuizId(answerObj.quiz_id)
      setAnswerNum(answerObj.answer_num)
      setIsAnswer(answerObj.is_answer)
      setAnswer(answerObj.answer)
      setAnswerImgPath(answerObj.answer_img_path)
    } else if (answerObj.quiz_id) {
      setAnswerId('')
      setQuizId(answerObj.quiz_id)
      setAnswerNum(answerObj.answer_num)
      setIsAnswer(false)
      setAnswer('')
      setAnswerImgPath('')
    } else {
      setAnswerId('')
      setQuizId('')
      setAnswerNum(answerObj.answer_num)
      setIsAnswer(false)
      setAnswer('')
      setAnswerImgPath('')
    }
  }, [answerItem])

  useEffect(() => {
    console.log(answer)
  }, [answer])

  return (
    <div>
      <input
        type="text"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />
    </div>
  )
}


export default CreateQuizAnswer