import React, { useState, useCallback, useEffect } from 'react';
import { useDebounce } from 'use-debounce';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import CompareArrowsSharpIcon from '@mui/icons-material/CompareArrowsSharp';
import IconButton from '@mui/material/IconButton';
import {currencyFormatter, convertCurrency} from './utils/utils';
import { getFlagEmoji } from './utils/currencyFlags';

const CustomAutoComplete = ({id, optionsList, value, setterFunc}) => {
    return (
        <Autocomplete
            sx={{width: "100%"}}
            options={optionsList}
            disableClearable
            id={id}
            value={value}
            onChange={ (event, newValue) => setterFunc(newValue)}
            isOptionEqualToValue={(option, value) => option.currCode === value.currCode}
            getOptionLabel={(option) => option.currCode}
            renderOption={(props, option) => (
                <Box component="li" {...props}>
                {option.currFlag} {option.currCode}
                </Box>
            )}
            renderInput={(params) => (
            <TextField {...params} variant="standard" width="100%" />
            )}
        />
    )
}

const CurrencyConverter = ({rates}) => {
    let currencyRates = Object.keys(rates.rates).sort().map(
        item => {
            return {currFlag: getFlagEmoji(item), currCode: item}
        }
    )

    const [converted, setConverted] = useState(0)
    const [fromCode, setFromCode] = useState(currencyRates[0])
    const [toCode, setToCode] = useState(currencyRates[0])
    const [amount, setAmount] = useState(1)
    const [amountDebounced] = useDebounce(amount, 800);

    const getConversion = useCallback( () => {
        setConverted(
            convertCurrency(rates.rates[toCode.currCode], rates.rates[fromCode.currCode], amountDebounced)
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
        <Stack spacing={2} display="flex" justifyContent="center" alignItems="center">
            <Box display="flex" justifyContent="center" alignItems="center">
                <Typography variant="h6" gutterBottom>
                    {currencyFormatter(amountDebounced, fromCode.currCode)} = {currencyFormatter(converted, toCode.currCode)}
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
            <Stack spacing={2} direction="row" display="flex" justifyContent="space-evenly" alignItems="center" width="100%">
                <CustomAutoComplete
                    id="currencies-from"
                    optionsList={currencyRates}
                    value={fromCode}
                    setterFunc={setFromCode}
                />
                <IconButton onClick={switchToFrom}>
                    <CompareArrowsSharpIcon/>
                </IconButton>
                <CustomAutoComplete
                    id="currencies-to"
                    optionsList={currencyRates}
                    value={toCode}
                    setterFunc={setToCode}
                />
            </Stack>
        </Stack>
    )
}

export default CurrencyConverter
