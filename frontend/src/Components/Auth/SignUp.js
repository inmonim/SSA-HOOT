import React, { useState } from 'react';
import Modal from 'react-modal';
import axios from 'axios';

Modal.setAppElement('#root'); // 모달을 루트 DOM 요소에 연결

function SignUp({ isOpen, onClose }) {

  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('');

  const handleSignUp = () => {

    const signUpData = {
      user_name: username,
      user_id: userId,
      password: password,
      role: role
    }

    axios.post('http://127.0.0.1:8000/users/create_user', signUpData)
      .then(response => {
        console.log(response)
      })
      .catch(error => {
        console.log(error)
      })
  }

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="SignUp Modal"
    >
      <h2>회원가입</h2>
      <input
        type="text"
        placeholder="사용자 이름"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="text"
        placeholder="ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <input
        type="role"
        placeholder="신분"
        value={role}
        onChange={(e) => setRole(e.target.value)}
      />
      <button onClick={handleSignUp}>회원가입</button>
    </Modal>
  );
}

export default SignUp;