import React, { useState, useEffect, useCallback } from 'react';
import CurrencyConverter from './components/currencyConverter';
import Box from '@mui/material/Box';
import CircularProgress from '@mui/material/CircularProgress';

function App() {
  const [currencies, setCurrencies] = useState([]);

  let getCurrencies = useCallback(async () => {
    await fetch('/currencies').then(res => res.json()).then(data => {
      setCurrencies(data);
    });
  }, [])

  useEffect(() => {
    getCurrencies()
  }, [getCurrencies]);

  return (
    <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh"
    >
      {
        currencies && currencies.success? <CurrencyConverter currencies={currencies.currencies}/> :
        <Box sx={{ display: 'flex' }}>
          <CircularProgress />
        </Box>
      }
    </Box>
  );
}

export default App;
