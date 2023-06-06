import React, {useState} from 'react';
import {AiOutlineDown, AiOutlineFileText, AiOutlineUp} from 'react-icons/ai';
import { Link } from 'react-router-dom';

function StockListElement(props) {
  const stock = props.stock;
  const growing = stock.change > 0;
  const [isDown, setDown] = useState(false);

  function handleClick() {
    setDown(!isDown);
  }

  return (
    <div>
      <div
        className={
          isDown ? 'StockListElement down' : 'StockListElement'
        }
      >
        <div className="symbol">{stock.ticker}</div>
        <div className="company">{stock.company_name}</div>
        <div className="price"> {stock.price}</div>
        <div className={growing ? 'change-green' : 'change-red'}>
          {stock.change}({growing ? '+' : ''}
          {stock.change_percent}%)
        </div>
        <div>
          <button className="dropdown-button" onClick={handleClick}>
            {isDown ? <AiOutlineUp /> : <AiOutlineDown />}
          </button>
        </div>
        <div>
          <Link to={"/stocks/"+stock.ticker}>
          <button>
            {<AiOutlineFileText />}
          </button>
          </Link>
        </div>
      </div>
      {isDown ? (
        <div className="details">
          <div className="grid">
            <div>Previous close: {stock.previous_close}</div>
            <div>Open: {stock.open_price}</div>
            <div>Volume: {stock.volume}</div>
          </div>
        </div>
      ) : (
        ''
      )}
    </div>
  );
}

export default StockListElement;
