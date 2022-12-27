import CurrencyApp from './components/currencyApp';
import { Navigate, useRoutes } from 'react-router-dom';
import {LoginPage, TopBarLogoutButton} from './components/pages/login';

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
  const loggedIn = localStorage.getItem('loggedIn') === 'true'
  const routing = useRoutes(routes(loggedIn));

  return (
    <>
      {routing}
    </>
  )
}

export default App;
