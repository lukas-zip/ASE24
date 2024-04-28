import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.less'
import { store } from './store';
import App from './App';
import { Provider } from 'react-redux';
import StateContextProvider from './pages/ClientHomePage/context';
// import '@/mock/userService'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <StateContextProvider>
        <App />
      </StateContextProvider>
    </Provider>
  </React.StrictMode>,
)
