import React, {useEffect, useState} from 'react';
import StockProvider from '../providers/StockProvider';
import { useParams } from 'react-router-dom';
import '../styles/StockPage.scss';
import StockChart from './StockChart';


function StockPage() {
  const [stock, setStock] = useState(null);
  let {ticker} = useParams();
  const growing = stock && stock.change > 0;

  
  useEffect(() => {
    StockProvider.getStock(ticker).then((stock) => {
      setStock(stock);
    });   

  }, [ticker]);

  return (
    <div className="StockPage-container">
      {stock === null ? ( 
        <div className="div-error">
          Searched stock does not exist.
        </div>  
      ) : (
        <div className="StockPage">
            <div className="data-container">
            <div className="symbol">Symbol: {stock.ticker}</div>
            <div className="company">Company name: {stock.company_name}</div>
            <div className="price">Stock price: {stock.price}</div>
            <div>
                Change:
                <div className={growing ? 'change-green' : 'change-red'}>
                {stock.change}({growing ? '+' : ''}{stock.change_percent}%)
                </div>
            </div> 
            <div>Previous close: {stock.previous_close}</div>
            <div>Open: {stock.open_price}</div>
            <div>Volume: {stock.volume}</div>
            </div>
            <div>
                  <StockChart data={stock.stock_history} growing={growing} />
            </div>
        </div>
      )
      }
    </div>
  );
}

export default StockPage;
