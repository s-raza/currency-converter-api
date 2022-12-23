import React, { useState, useCallback, useEffect } from 'react';
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import {currencyFormatter} from './utils';
import { convertCurrency } from './utils';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

const colHeaders = [
    {field: 'currCode', headerName: 'Code', width: 120},
    {field: 'rate', headerName: 'Rate', width: 120},
]

const GridCurrencyRates = ({rates}) => {
    const [baseCurrency, setBaseCurrency] = useState(rates.base_currency)
    const [rows, setRows] = useState([])
    let currencyList = Object.keys(rates.rates).sort()

    const getRows = useCallback( () => {
        let formatted_rows = []
        for (const [key, value] of Object.entries(rates.rates)) {
            formatted_rows.push({'id': key, 'currCode': key, 'rate': currencyFormatter(convertCurrency(value, rates.rates[baseCurrency]), key)})
        }
        setRows(formatted_rows)
      }, [baseCurrency])

    useEffect(() => {
        getRows()
      }, [baseCurrency, getRows]);

      return (
        <Box sx={{ height: 400, width: '100%' }}>
        <Autocomplete
                options={currencyList}
                disableClearable
                id="currencies-from"
                value={baseCurrency}
                onChange={ (event, newValue) => setBaseCurrency(newValue)}
                sx={{ width: 100 }}
                renderInput={(params) => (
                <TextField {...params} variant="standard" />
                )}
            />
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
        </Box>
      )
}

export default GridCurrencyRates
