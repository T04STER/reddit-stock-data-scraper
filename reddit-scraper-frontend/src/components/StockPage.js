import React, {useEffect, useState} from 'react';
import StockProvider from '../providers/StockProvider';
import {useParams} from 'react-router-dom';
import '../styles/StockPage.scss';
import StockChart from './StockChart';
import {AiOutlineLoading} from 'react-icons/ai';

function StockPage() {
  const [stock, setStock] = useState(undefined);
  let {ticker} = useParams();
  const growing = stock && stock.change > 0;

  useEffect(() => {
    StockProvider.getStock(ticker).then((stock) => {
      setStock(stock);
    });
  }, [ticker]);

  const renderStock = () => {
    return (
      <div className="StockPage">
        <div className="data-container">
          <div className="symbol">Symbol: {stock.ticker}</div>
          <div className="company">
            Company name: {stock.company_name}
          </div>
          <div className="price">Stock price: {stock.price}</div>
          <div>
            Change:
            <div className={growing ? 'change-green' : 'change-red'}>
              {stock.change}({growing ? '+' : ''}
              {stock.change_percent}%)
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
    );
  };
  const renderError = () => {
    return (
      <div className="div-error">
        {' '}
        Searched stock does not exist.{' '}
      </div>
    );
  };
  const renderLoading = () => {
    return (
      <div className="div-loading">
        Searched stock is being loaded.
        <div className="loading-spinner">
          <AiOutlineLoading />
        </div>
      </div>
    );
  };

  return (
    <div className="StockPage-container">
      {stock === undefined
        ? renderLoading()
        : stock === null
        ? renderError()
        : renderStock()}
    </div>
  );
}

export default StockPage;
