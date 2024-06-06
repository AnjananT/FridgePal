import { useState } from 'react'
import './App.css'
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Home from './pages/Home'
import RecipeEdit from './pages/RecipeEdit'
import MenuBar from './components/MenuBar'

import "./fonts/SoleilRegular.otf";
function App() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <Router>
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/recipeedit" element={<RecipeEdit/>} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
