import React, {useState} from 'react'
import {AiOutlineSearch} from 'react-icons/ai';
import { Link, useNavigate } from 'react-router-dom';
function SearchBar() {
  const [input, setInput] = useState('enter ticker');
  const navigate = useNavigate();

  const handleInputChange = (event) => {
        setInput(event.target.value);
    }  
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      navigate(`/stocks/${input}`);
    }
  };
  return (
    <div className='SearchBar'>
        <input
            type="text"
            className="search-input"
            placeholder="enter ticker"
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            value={input}
        />
        <Link to={"/stocks/"+input}>
            <button><AiOutlineSearch/></button>
        </Link>
    </div>
  )
}

export default SearchBar