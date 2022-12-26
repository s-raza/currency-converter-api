import { useState, useEffect, useCallback} from 'react';
import {
    Box,
    Button,

} from "@mui/material"


const LoginPage = () => {
    const [loggedIn, setLoggedIn] = useState(false)
    const [buttonText, setButtonText] = useState("Login")

    const handleLogin = (event) => {
        setLoggedIn(!loggedIn)
    }

    const updateButtonText = useCallback(
        () => {
            setButtonText(loggedIn? "Log Out": "Login")
    },[loggedIn])

    useEffect(updateButtonText, [loggedIn, updateButtonText])

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
            <Button variant={loggedIn? "contained": "outlined"} onClick={handleLogin}>{buttonText}</Button>
        </Box>
    )
}

export default LoginPage
