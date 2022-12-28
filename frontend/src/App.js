import CurrencyApp from './components/currencyApp';
import { Navigate, useRoutes } from 'react-router-dom';
import {LoginPage, TopBarLogoutButton} from './components/pages/login';
import { LoggedInContext, TokenContext } from './components/contexts';
import { useState, useEffect } from 'react';

const routes = (loggedIn) =>
  [
    {
      path: "/",
      element: loggedIn?
      <TopBarLogoutButton>
        <CurrencyApp />
      </TopBarLogoutButton>:
      <Navigate to="login" />
    },
    {
      path: "login",
      element: <LoginPage navigateTo="/" />
    }
  ]


function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [token, setToken] = useState(false)
  const routing = useRoutes(routes(loggedIn))

  const readToken = () => {
    if (localStorage.getItem('loggedIn') === 'true') {
      setLoggedIn(true)
      setToken(true)
    }
  }

  useEffect(() => {
    readToken()
  }, [])

  return (
    <LoggedInContext.Provider value={{ loggedIn, setLoggedIn }}>
      <TokenContext.Provider value={{ token, setToken }}>
        {routing}
      </TokenContext.Provider>
    </LoggedInContext.Provider>
  )
}

export default App;
