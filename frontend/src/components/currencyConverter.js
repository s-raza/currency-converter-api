import React, { useState, useCallback } from 'react';

const CurrencyDropDown = ({currencies, onSelect, label}) => {

    return (
    <div>
    {label}: <select onChange={onSelect}>
        {
            currencies.map(
                item => {
                    return (
                        <option key = {item} value={item}>
                            {item}
                        </option>
                    )
                }
            )
        }
    </select>
    </div>
    )
}

const CurrencyConverter = ({currencies}) => {
    const [converted, setConverted] = useState({})
    const [fromCode, setFromCode] = useState(currencies[0])
    const [toCode, setToCode] = useState(currencies[0])
    const [amount, setAmount] = useState('')

    const getConversion = useCallback(async () => {
        await fetch(`/currencies/convert/${fromCode}/${toCode}?amount=${amount}`).then(res => res.json()).then(data => {
            setConverted(data);
        });
      }, [fromCode, toCode, amount])

    const handleFromCode = (event) => {
        setFromCode(event.target.value)
    }

    const handleToCode = (event) => {
        setToCode(event.target.value)
    }

    const handleAmount = (event) => {
        setAmount(event.target.value)
    }

    return (
        <div>
            <CurrencyDropDown currencies={currencies} onSelect={handleFromCode} label="From"/>
            <CurrencyDropDown currencies={currencies} onSelect={handleToCode} label="To" />
            <input type="text" placeholder='Amount' value={amount} onChange={handleAmount} />
            <button onClick={getConversion}>Convert</button>
            <div>
                Converted: {converted.converted}
            </div>
        </div>
    )
}

export default CurrencyConverter
