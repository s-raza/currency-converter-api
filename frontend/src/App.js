import { useState, useEffect, useCallback } from 'react';
import CurrencyConverter from './components/currencyConverter';
import {Box} from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import GridCurrencyRates from './components/currencyDataGrid';
import Stack from '@mui/material/Stack';
import { useNavigate } from "react-router-dom";
import { LoginButton } from './components/pages/login';
import TopBar from './components/appBar';

function App() {
  let navigate = useNavigate();
  const [rates, setRates] = useState({});
  const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true')

  let getRates = useCallback(async () => {
    await fetch('/currencies/rates').then(res => res.json()).then(data => {
      setRates(data);
    });
  }, [])

  const handleLogout = () => {
    setLoggedIn(false)
    localStorage.setItem('loggedIn', false)
  }

  useEffect(() => {
    if (!loggedIn){
      return navigate("login");
   }
    getRates()
  }, [loggedIn, getRates, navigate]);

  return (
    <>
    <TopBar loginButton={<LoginButton loggedIn={loggedIn} onClick={handleLogout} buttonText="Log Out" />}/>
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh"
    >
      {
        rates && rates.success?
        <Stack spacing={2}>
        <CurrencyConverter rates={rates}/>
        <GridCurrencyRates rates={rates}/>
        </Stack> :
        <Box sx={{ display: 'flex' }}>
          <CircularProgress />
        </Box>
      }
    </Box>
    </>
  );
}

export default App;
