import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Home from './Pages/Home'
import CreateQuizShowPage from './Pages/CreateQuizShowPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="create_quiz" element={<CreateQuizShowPage />} />
      </Routes>
    </Router>
  );
}

export default App;