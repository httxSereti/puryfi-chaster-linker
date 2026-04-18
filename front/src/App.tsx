import { Routes, Route } from 'react-router-dom'
import Main from './pages/Main'
import Configuration from './pages/Configuration'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/extension/main" element={<Main />} />
      <Route path="/extension/configuration" element={<Configuration />} />
    </Routes>
  )
}

export default App
