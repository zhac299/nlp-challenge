import React, { useState } from 'react';
import './UserInput.css';
import axios from 'axios';

const UserInput = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const chatbot = document.getElementById('chatbot');
  const conversation = document.getElementById('conversation');
  const inputForm = document.getElementById('input-form');
  const inputField = document.getElementById('input-field');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', { input });
      setResult(response.data.result);
          // Clear input field
          inputField.value = '';
          const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

          // Add user input to conversation
          let message = document.createElement('div');
          message.classList.add('chatbot-message', 'user-message');
          message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${input}</p>`;
          conversation.appendChild(message);

          let message2 = document.createElement('div');
          message2.classList.add('chatbot-message', 'chatbot-text');
          message2.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${response.data.result}</p>`;
          conversation.appendChild(message2);

    } catch (error) {
      console.error('Error:', error);
    }


  };

  return (
    <div>
      <head>
        <title>Jaguar Land Rover</title>
        <link rel="stylesheet" href="UserInput.css"></link>
      </head>
      <body>
        <div class="chatbot-container">
          <div id="header">
            <h1>JLR</h1>
          </div> 
        <div>
        <div id="conversation">
              <div class="chatbot-message">
                <p class="chatbot-text">Hello! 👋 Welcome to JLR's digital shop!</p>
              </div>
            </div>
          </div>  
          <form id="input-form" onSubmit={handleSubmit}>
            <message-container>
              <input id="input-field" type="text" placeholder='type here' value={input} onChange={(e) => setInput(e.target.value)} />
              <button id="submit-button" class="button1" type="submit">Enter</button>
            </message-container>
          </form>
        </div>
      </body>
    </div>
  );
};

export default UserInput;