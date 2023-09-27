import React, { useEffect, useState } from "react";

function CreateQuizAnswer({ answerObj }) {

  const [answerId, setAnswerId] = useState('');
  const [quizId, setQuizId] = useState('');
  const [answerNum, setAnswerNum] = useState('');
  const [isAnswer, setIsAnswer] = useState(false);
  const [answer, setAnswer] = useState('');
  const [answerImgPath, setAnswerImgPath] = useState('');

  useEffect(() => {

    if (answerObj != null) {
      setAnswerId(answerObj.id)
      setQuizId(answerObj.quiz_id)
      setAnswerNum(answerObj.answer_num)
      setIsAnswer(answerObj.is_answer)
      setAnswer(answerObj.answer)
      setAnswerImgPath(answerObj.answer_img_path)
    }
  })

  return (
    <div>
      <input
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
      />
    </div>
  )
}


export default CreateQuizAnswer