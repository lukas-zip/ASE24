import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.less'
import { store } from './store';
import App from './App';
import { Provider } from 'react-redux';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
)
