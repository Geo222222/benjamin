import React from 'react';
import ReactDOM from 'react-dom/client';
import { App } from './App';
import { installProductPolish } from './polish';
import './styles.css';
import './theme.css';
import './polish.css';

installProductPolish();

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);