import React, { useState, useCallback, useEffect } from 'react';
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import {currencyFormatter} from './utils';
import Typography from '@mui/material/Typography';

const colHeaders = [
    {field: 'currCode', headerName: 'Code', width: 120},
    {field: 'rate', headerName: 'Rate', width: 120},
]

const GridCurrencyRates = () => {
    const [rates, setRates] = useState({})

    const getRates = useCallback(async () => {
        await fetch(`/currencies/rates`).then(res => res.json()).then(data => {
            setRates(data);
        });
      }, [])

    useEffect(() => {
        getRates()
      }, [getRates]);

    let rows = []

    if (rates && rates.success) {
        for (const [key, value] of Object.entries(rates.rates)) {
        rows.push({'id': key, 'currCode': key, 'rate': currencyFormatter(value, key)})
        }
    }

      return (
        <Box sx={{ height: 400, width: '100%' }}>
            <Typography gutterBottom align='center'>
                Current Rates, Base Currency: {rates.base_currency}
            </Typography>
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
