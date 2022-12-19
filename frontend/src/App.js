import React, { useState, useEffect, useCallback } from 'react';

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
      <ul>
      {
          currencies && currencies.success && currencies.currencies.map(
            (item) => {
              return(
                <li key={item}>{item}</li>
              )
            }
          )
        }
      </ul>
    </div>
  );
}

export default App;
