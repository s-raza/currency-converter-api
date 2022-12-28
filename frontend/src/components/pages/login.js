import { useState, useEffect, useCallback} from 'react';
import {
    Box,
    Button,

} from "@mui/material"
import { useNavigate } from "react-router-dom";
import TopBar from '../appBar';
import { LoggedInContext, TokenContext } from '../contexts';
import { useContext } from 'react';

export const LoginButton = ({loggedIn, onClick, buttonText}) => {
    return(
        <Button variant={loggedIn? "contained": "outlined"} onClick={onClick}>{buttonText}</Button>
    )
}

export const TopBarLogoutButton = ({children}) => {
    let navigate = useNavigate();
    const loggedIn = useContext(LoggedInContext)
    const token = useContext(TokenContext)

    const handleLogout = () => {
        loggedIn.setLoggedIn(false)
        token.setToken(false)
    }

    const setStorage = useCallback(
        () => {
            localStorage.setItem('loggedIn', loggedIn.loggedIn)
        }, [loggedIn]
    )

    useEffect(() => {
        setStorage()
        if(!loggedIn.loggedIn) {return navigate("login")}
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
    const loggedIn = useContext(LoggedInContext)
    const token = useContext(TokenContext)
    const [buttonText, setButtonText] = useState("Login")

    const handleLogin = (event) => {
        loggedIn.setLoggedIn(!loggedIn.loggedIn)
        token.setToken(!token.token)
    }

    const updateOnLogin = useCallback(
        () => {
            setButtonText(loggedIn.loggedIn? "Log Out": "Login")
            localStorage.setItem('loggedIn', loggedIn.loggedIn)
            if(loggedIn.loggedIn) {
                return navigate(navigateTo);
            }
    },[loggedIn, navigate, navigateTo])

    useEffect(updateOnLogin, [loggedIn, updateOnLogin])

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
            <LoginButton loggedIn={loggedIn.loggedIn} onClick={handleLogin} buttonText={buttonText}/>
        </Box>
    )
}
