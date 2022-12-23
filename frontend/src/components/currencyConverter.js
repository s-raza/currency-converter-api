import React, { useState, useCallback, useEffect } from 'react';
import { useDebounce } from 'use-debounce';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import CompareArrowsSharpIcon from '@mui/icons-material/CompareArrowsSharp';
import IconButton from '@mui/material/IconButton';
import {currencyFormatter, convertCurrency} from './utils';

const CurrencyConverter = ({rates}) => {
    let currencies = Object.keys(rates.rates).sort()
    const [converted, setConverted] = useState(0)
    const [fromCode, setFromCode] = useState(currencies[0])
    const [toCode, setToCode] = useState(currencies[0])
    const [amount, setAmount] = useState(1)
    const [amountDebounced] = useDebounce(amount, 800);

    const getConversion = useCallback( () => {
        setConverted(
            convertCurrency(rates.rates[toCode], rates.rates[fromCode], amountDebounced)
        )
      }, [rates.rates, fromCode, toCode, amountDebounced]
    )

    const switchToFrom = () => {
        setFromCode(toCode)
        setToCode(fromCode)
    }

    useEffect(() => {
        getConversion()
      }, [amountDebounced, fromCode, toCode, getConversion]);

    return (
        <Stack spacing={2}>
            <Box display="flex" justifyContent="center" alignItems="center">
                <Typography variant="h6" gutterBottom>
                    {currencyFormatter(amountDebounced, fromCode)} = {currencyFormatter(converted, toCode)}
                </Typography>
            </Box>
            <Box component="form" noValidate autoComplete="off" display="flex" justifyContent="center" alignItems="center">
                <TextField
                required
                id="outlined-number"
                label="Amount"
                type="number"
                inputProps={{min: 0, style: { textAlign: 'center', fontSize: 25, padding: 1 }}}
                value={amount}
                onChange={event => setAmount(event.target.value? event.target.value: 1)}
                onFocus={event => event.target.select()}
                />
            </Box>
            <Stack direction="row" spacing={2} display="flex" justifyContent="center" alignItems="center">
                <Autocomplete
                    options={currencies}
                    disableClearable
                    id="currencies-from"
                    value={fromCode}
                    onChange={ (event, newValue) => setFromCode(newValue)}
                    sx={{ width: 100 }}
                    renderInput={(params) => (
                    <TextField {...params} variant="standard" />
                    )}
                />
                <IconButton onClick={switchToFrom}>
                    <CompareArrowsSharpIcon/>
                </IconButton>
                <Autocomplete
                    options={currencies}
                    disableClearable
                    id="currencies-to"
                    value={toCode}
                    onChange={ (event, newValue) => setToCode(newValue)}
                    sx={{ width: 100 }}
                    renderInput={(params) => (
                    <TextField {...params} variant="standard" />
                    )}
                />
            </Stack>
        </Stack>
    )
}

export default CurrencyConverter
