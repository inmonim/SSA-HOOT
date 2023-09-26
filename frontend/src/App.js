import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './Pages/Home'
import CreateQuizShowPage from './Pages/CreateQuizShowPage'
import CreateQuizPage from './Pages/CreateQuizPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="create_quiz_show" element={<CreateQuizShowPage />} />
        <Route path="create_quiz" element={<CreateQuizPage />} />
      </Routes>
    </Router>
  );
}

export default App;