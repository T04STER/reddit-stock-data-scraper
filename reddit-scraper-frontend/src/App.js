import './styles/App.scss';
import TopBar from './components/TopBar';
import StockList from './components/StockList';
import StockPage from './components/StockPage';
import { Route, Routes } from 'react-router-dom';



function App() {
  console.log(process.env);
  return (
    <div className="App">
        <TopBar />
        <Routes>
          <Route path='/' element={<StockList />}/>
          <Route path='/stocks/:ticker' element={<StockPage />}/>
        </Routes>
      
    </div>
  );
}

export default App;