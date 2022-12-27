import { useState, useEffect, useCallback } from 'react';
import {Box} from '@mui/material';
import CircularProgress from '@mui/material/CircularProgress';
import Stack from '@mui/material/Stack';
import CurrencyConverter from './currencyConverter';
import GridCurrencyRates from './currencyDataGrid';

const CurrencyApp = () => {
    const [rates, setRates] = useState({});

    let getRates = useCallback(async () => {
        await fetch('/currencies/rates').then(res => res.json()).then(data => {
        setRates(data);
        });
    }, [])

    useEffect(() => {
        getRates()
    }, [getRates]);

    return(
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
    )
}

export default CurrencyApp
