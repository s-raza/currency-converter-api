import React, { useState, useEffect, useCallback } from 'react';
import CurrencyConverter from './components/currencyConverter';

function App() {
  const [currencies, setCurrencies] = useState([]);

  let getCurrencies = useCallback(async () => {
    await fetch('/currencies/').then(res => res.json()).then(data => {
      setCurrencies(data);
    });
  }, [])

  useEffect(() => {
    getCurrencies()
  }, [getCurrencies]);

  console.log(currencies)

  return (
    <div className="App">
      {
        currencies && currencies.success? <CurrencyConverter currencies={currencies.currencies}/> :
        <>Loading...</>
      }
    </div>
  );
}

export default App;
