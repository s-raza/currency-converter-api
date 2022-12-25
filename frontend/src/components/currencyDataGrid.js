import React, { useState, useCallback, useEffect } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import {currencyFormatter} from './utils/utils';
import { convertCurrency } from './utils/utils';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import { useDebounce } from 'use-debounce';
import Stack from '@mui/material/Stack';

const colHeaders = [
    {field: 'currCode', headerName: 'Code', width: 120},
    {field: 'rate', headerName: 'Rate', width: 300},
]

const GridCurrencyRates = ({rates}) => {
    const [baseCurrency, setBaseCurrency] = useState(rates.base_currency)
    const [rows, setRows] = useState([])
    const [amount, setAmount] = useState(1)
    const [amountDebounced] = useDebounce(amount, 800);
    let currencyList = Object.keys(rates.rates).sort()

    const getRows = useCallback( () => {
        let formatted_rows = []
        for (const [key, value] of Object.entries(rates.rates)) {
            formatted_rows.push({'id': key, 'currCode': key, 'rate': currencyFormatter(convertCurrency(value, rates.rates[baseCurrency], amountDebounced), key)})
        }
        setRows(formatted_rows)
      }, [rates.rates, amountDebounced, baseCurrency])

    useEffect(() => {
        getRows()
      }, [amountDebounced, baseCurrency, getRows]);

    return (
    <Stack spacing={2} display="flex" justifyContent="center" alignItems="center" sx={{ height: 400, width: '100%' }}>
        <Stack direction="row" spacing={2} display="flex" justifyContent="space-evenly" alignItems="center" width='100%'>
            <Autocomplete
                sx={{width: "100%"}}
                options={currencyList}
                disableClearable
                id="currencies-from"
                value={baseCurrency}
                onChange={ (event, newValue) => setBaseCurrency(newValue)}
                renderInput={(params) => (
                <TextField {...params} variant="standard" width="100%"/>
                )}
            />
            <TextField
                required
                sx={{width: "100%"}}
                id="outlined-number"
                label="Amount"
                type="number"
                inputProps={{min: 0, style: { textAlign: 'center', fontSize: 20, padding: 1}}}
                value={amount}
                onChange={event => setAmount(event.target.value? event.target.value: 1)}
                onFocus={event => event.target.select()}
                />
        </Stack>
        <DataGrid
            rows={rows}
            rowHeight={30}
            headerHeight={35}
            density='compact'
            columns={colHeaders}
            disableSelectionOnClick
            experimentalFeatures={{ newEditingApi: true }}
            sortModel={[{field: 'currCode', sort: 'asc'}]}
        />
    </Stack>
    )
}

export default GridCurrencyRates
