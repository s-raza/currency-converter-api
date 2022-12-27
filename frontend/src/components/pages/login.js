import { useState, useEffect, useCallback} from 'react';
import {
    Box,
    Button,

} from "@mui/material"


const LoginPage = () => {
    const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true')
    const [buttonText, setButtonText] = useState("Login")

    const handleLogin = (event) => {
        setLoggedIn(!loggedIn)
    }

    const updateButtonText = useCallback(
        () => {
            setButtonText(loggedIn? "Log Out": "Login")
            localStorage.setItem('loggedIn', loggedIn)
    },[loggedIn])

    useEffect(updateButtonText, [loggedIn, updateButtonText])

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
            <Button variant={loggedIn? "contained": "outlined"} onClick={handleLogin}>{buttonText}</Button>
        </Box>
    )
}

export default LoginPage
