import React, { useState } from 'react';
import Modal from 'react-modal';
import axios from 'axios';

Modal.setAppElement('#root'); // 모달을 루트 DOM 요소에 연결

function Login({ isOpen, onClose }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {

    const login_data = {
      username: username,
      password: password,
    }

    const config = {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }

    }

    axios.post('http://127.0.0.1:8000/users/login', login_data, config)
      .then(response => {

        console.log(response)
      })
      .catch(error => {
        console.log(login_data)
        console.log(error)
      })
  }

  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={onClose}
      contentLabel="Login Modal"
    >
      <h2>로그인</h2>
      <input
        type="text"
        placeholder="사용자 이름"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>로그인</button>
    </Modal>
  );
}

export default Login;