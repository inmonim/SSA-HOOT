import React, { useState } from "react";

import Login from "../Components/Auth/Login";
import SignUp from "../Components/Auth/SignUp";

function Home() {

  const [loginModalOpen, setLoginModalOpen] = useState(false);
  const [signUpModalOpen, setSignUpModalOpen] = useState(false);

  const openSignUpModal = () => {
    setSignUpModalOpen(true);
  };
  const openLoginModal = () => {
    setLoginModalOpen(true);
  };

  const closeModal = () => {
    setLoginModalOpen(false);
    setSignUpModalOpen(false);
  }

  return (
    <div>
      <div>
        <h1> 호오옴 페이지 </h1>
        <button onClick={openLoginModal}>로그인</button>
        <Login isOpen={loginModalOpen} onClose={closeModal} />
        <button onClick={openSignUpModal}>회원가입</button>
        <SignUp isOpen={signUpModalOpen} onClose={closeModal} />
      </div>
    </div>
  )
}

export default Home;