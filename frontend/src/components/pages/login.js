import { useState, useEffect, useCallback} from 'react';
import {
    Box,
    Button,

} from "@mui/material"
import { useNavigate } from "react-router-dom";
import TopBar from '../appBar';

export const LoginButton = ({loggedIn, onClick, buttonText}) => {
    return(
        <Button variant={loggedIn? "contained": "outlined"} onClick={onClick}>{buttonText}</Button>
    )
}

export const TopBarLogoutButton = ({children}) => {
    let navigate = useNavigate();
    const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true')

    const handleLogout = () => {
        setLoggedIn(false)
    }

    const setStorage = useCallback(
        () => {
            localStorage.setItem('loggedIn', loggedIn)
        }, [loggedIn]
    )

    useEffect(() => {
        setStorage()
        if(!loggedIn) {return navigate("login")}
        }, [loggedIn, navigate, setStorage]
    )

    return(
        <>
        <TopBar loginButton={<LoginButton loggedIn={loggedIn} onClick={handleLogout} buttonText="Log Out" />}/>
        {children}
        </>
    )
}

export const LoginPage = ({navigateTo}) => {
    let navigate = useNavigate();
    const [loggedIn, setLoggedIn] = useState(localStorage.getItem('loggedIn') === 'true')
    const [buttonText, setButtonText] = useState("Login")

    const handleLogin = (event) => {
        setLoggedIn(!loggedIn)
    }

    const updateButtonText = useCallback(
        () => {
            setButtonText(loggedIn? "Log Out": "Login")
            localStorage.setItem('loggedIn', loggedIn)
            if(loggedIn) {
                return navigate(navigateTo);
            }
    },[loggedIn, navigate, navigateTo])

    useEffect(updateButtonText, [loggedIn, updateButtonText])

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
            <LoginButton loggedIn={loggedIn} onClick={handleLogin} buttonText={buttonText}/>
        </Box>
    )
}
