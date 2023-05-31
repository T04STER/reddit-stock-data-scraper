import React from 'react';
import { Link } from 'react-router-dom';
import {AiOutlineHome} from 'react-icons/ai';
import SearchBar from './SearchBar';
function TopBar() {
  return (
    <div className="TopBar">
      <h1>Reddit stock data scrapper</h1>
      <div className='nav-menu'>
        <div>
          <Link className='Link' to='/'>
            <button><AiOutlineHome/></button>
          </Link>
        </div>
        <SearchBar/>
      </div>
    </div>
  );
}

export default TopBar;
