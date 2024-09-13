import { HashRouter, Route, Routes } from 'react-router-dom';
import { Home } from './components/pages/candidate';
import { Interviews } from './components/pages/common/Interviews';

const App = () =>
  <HashRouter>
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path="/interviews" element={<Interviews />} />
    </Routes>
  </HashRouter>


export default App
