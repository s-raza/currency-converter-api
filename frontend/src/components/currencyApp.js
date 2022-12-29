import React from 'react';
import {useState, useEffect, useCallback, useContext} from 'react';
import {Box} from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import Stack from '@mui/material/Stack';
import CurrencyConverter from './currencyConverter';
import GridCurrencyRates from './currencyDataGrid';
import {TokenContext} from './contexts';
import axios from 'axios';

const CurrencyApp = () => {
  const [rates, setRates] = useState();
  const token = useContext(TokenContext);

  const getRates = useCallback(async () => {
    const headers = {
      'Authorization': `Bearer ${token.token}`,
    };

    await axios.get(
        '/currencies/rates',
        {headers}).then((response) => {
      setRates(response.data);
    })
        .catch((error) => {
          console.log(error.toJSON());
          token.setToken('');
        });
  }, [token]);

  useEffect(() => {
    getRates();
  }, [getRates]);

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh">
      {
            rates && rates.success?
            <Stack spacing={2}>
              <CurrencyConverter rates={rates}/>
              <GridCurrencyRates rates={rates}/>
            </Stack> :
            <Box sx={{display: 'flex'}}>
              <CircularProgress />
            </Box>
      }
    </Box>
  );
};

export default CurrencyApp;
