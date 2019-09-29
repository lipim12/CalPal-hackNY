import React from 'react';
import './App.css';

// import LoginPage from './components/LoginPage.js';
import LandingPage from './components/LandingPage.js';

function App(){
  return (
    
    <div style={{ backgroundColor: '#45db4b' }}>
      <p style={{ fontFamily:'bebas', color:'#45db4b', backgroundColor: 'white', fontWeight: '300', paddingLeft: '70px', paddingBottom: '30px' }}>CalPal</p>
      <LandingPage/>
    </div>
  );
}

export default App;
