import React from 'react';
import CurrencyApp from './components/currencyApp';
import {Navigate, useRoutes} from 'react-router-dom';
import {LoginPage, TopBarLogoutButton} from './components/pages/login';
import {TokenContext} from './components/contexts';
import {useState, useEffect} from 'react';


const routes = (token) =>
  [
    {
      path: '/',
      element: ['', false, null, undefined].includes(token) ?
      <Navigate to="login" />:
        <TopBarLogoutButton>
          <CurrencyApp />
        </TopBarLogoutButton>,
    },
    {
      path: 'login',
      element: <LoginPage navigateTo="/" />,
    },
  ];


function App() {
  const [token, setToken] = useState('');

  const readToken = () => {
    const storetoken = localStorage.getItem('token');

    if (storetoken !== null) {
      setToken(storetoken);
    }
  };

  useEffect(() => {
    readToken();
  }, []);

  if (token === false) {
    localStorage.removeItem('token');
  }

  const routing = useRoutes(routes(token));

  return (
    <TokenContext.Provider value={{token, setToken}}>
      {routing}
    </TokenContext.Provider>
  );
}

export default App;
