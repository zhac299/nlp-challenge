import React, { useState } from 'react';
import axios from 'axios';

const UserInput = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', { input });
      setResult(response.data.result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>
          Input:
          <input type="text" value={input} onChange={(e) => setInput(e.target.value)} />
        </label>
        <button type="submit">Submit</button>
      </form>
      <div>
        Result: {result}
      </div>
    </div>
  );
};

export default UserInput;