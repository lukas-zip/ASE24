import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const baseURL = 'http://127.0.0.1:5000'; // Change this to the IP of your backend container

  const handleLogin = async () => {
    try {
        const response = await axios.post(`${baseURL}/login`, {
            email: email,
            password: password,
        });
        console.log('Response:', response); // Log the entire response object
        if (response.data && response.data.message === 'Login successful') {
            // Handle successful login (e.g., redirect to another page)
            console.log('Login successful');
            // Redirect or set some state indicating successful login
        } else {
            console.error('Unexpected response from server:', response.data);
            setErrorMessage('An unexpected response occurred during login.');
        }
    } catch (error) {
        console.error('Login error:', error.response);
        if (error.response && error.response.data) {
            setErrorMessage(error.response.data.error);
        } else {
            setErrorMessage('An error occurred during login.');
        }
    }
};


  return (
    <div className="App">
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default App;