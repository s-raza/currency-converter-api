import React, { useState, useCallback, useEffect } from 'react';

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
    const [amount, setAmount] = useState(0)

    const getConversion = useCallback(async () => {
        await fetch(`/currencies/convert/${fromCode}/${toCode}?amount=${amount}`).then(res => res.json()).then(data => {
            setConverted(data);
        });
      }, [fromCode, toCode, amount])

    const handleChange = (event, setter) => {
        setter(event.target.value)
    }

    useEffect(() => {
        getConversion()
      }, [amount, fromCode, toCode]);

    return (
        <div>
            <CurrencyDropDown currencies={currencies} onSelect={ (event) => handleChange(event, setFromCode)} label="From"/>
            <CurrencyDropDown currencies={currencies} onSelect={ (event) => handleChange(event, setToCode)} label="To" />
            <input type="text" placeholder='Amount' value={amount} onChange={ (event) => handleChange(event, setAmount)} />
            <div>
                Converted: {converted.converted}
            </div>
        </div>
    )
}

export default CurrencyConverter
