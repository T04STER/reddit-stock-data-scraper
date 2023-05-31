import React, {useEffect, useState} from 'react';
import StockListElement from './StockListElement';
import StockProvider from '../providers/StockProvider';

function StockList() {
  const [stockList, setStockList] = useState([]);
  useEffect(() => {
    StockProvider.getStocks().then((stocks) => {
      setStockList(stocks);
    });
  }, []);

  return (
    <div className="StockList">
      {stockList.map((stock) => (
        <StockListElement key={stock.id} stock={stock} />
      ))}
    </div>
  );
}

export default StockList;
