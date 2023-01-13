import React from 'react';
import {useState, useEffect, useCallback, forwardRef} from 'react';
import {
  Avatar,
  Box,
  Button,
  TextField,
  Link,
  Typography,
  Container,
  CssBaseline,
  Snackbar,
  CircularProgress,
} from '@mui/material';
import {LoadingButton} from '@mui/lab';
import MuiAlert from '@mui/material/Alert';
import {useNavigate} from 'react-router-dom';
import TopBar from '../appBar';
import {TokenContext} from '../contexts';
import {useContext} from 'react';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import axios from 'axios';

const Alert = forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export const LoginButton = ({loggedIn, onClick, buttonText}) => {
  return (
    <Button
      variant={loggedIn? 'contained': 'outlined'}
      onClick={onClick}>{buttonText}
    </Button>
  );
};

export const TopBarLogoutButton = ({children}) => {
  const token = useContext(TokenContext);

  const handleLogout = () => {
    token.setToken(false);
  };

  return (
    <>
      <TopBar
        loginButton={<LoginButton loggedIn={token.token}
          onClick={handleLogout}
          buttonText="Log Out" />}/>
      {children}
    </>
  );
};

const theme = createTheme();

function Copyright(props) {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center" {...props}>
      <Link
        color="inherit"
        href="https://github.com/s-raza/currency-converter-api/"
        target={'new'}>
        GitHub
      </Link>
    </Typography>
  );
}

export const LoginPage = ({navigateTo}) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [snackbar, setSnackbar] = useState(
      {
        openSnackbar: false,
        msgSnackbar: '',
        vertical: 'bottom',
        horizontal: 'left',
      },
  );
  const [loadingButton, setLoadingButton] = useState(false);
  const {vertical, horizontal, openSnackbar, msgSnackbar} = snackbar;
  const token = useContext(TokenContext);

  const handleSnackbarClose = () => {
    setSnackbar({...snackbar, openSnackbar: false});
  };

  const handleUsername = (event) => {
    event.preventDefault();
    setUsername(event.target.value);
  };

  const handlePassword = (event) => {
    event.preventDefault();
    setPassword(event.target.value);
  };

  const handleLogin = async (event) => {
    if (event) {
      event.preventDefault();
    }

    setLoadingButton(true);

    const data = {
      client_id: '',
      client_secret: '',
      grant_type: '',
      scopes: '',
      username: username,
      password: password,
    };

    const urlEncoded = new URLSearchParams(data);

    const headers = {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded',
    };

    const getToken = async () => {
      await axios
          .post(
              '/token',
              urlEncoded,
              {headers: headers},
          ).then((response) => {
            token.setToken(response.data.access_token);
          })
          .catch((error) => {
            setLoadingButton(false);
            console.log(error.toJSON());
            let msg = '';

            switch (error.response.status) {
              case 401:
                msg = 'Incorrect Username or Password';
                break;
              case 404:
                msg = ` API endpoint: '${error.config.url}' not found`;
                break;
              default:
                msg = `${error.code}: ${error.message}`;
            }

            setSnackbar(
                {...snackbar,
                  openSnackbar: true,
                  msgSnackbar: msg,
                },
            );
            token.setToken(false);
          });
    };

    await getToken();
    setLoadingButton(false);
  };

  const updateOnLogin = useCallback(
      () => {
        if (!['', false, null, undefined].includes(token.token)) {
          localStorage.setItem('token', token.token);
          return navigate(navigateTo);
        }
      }, [token, navigate, navigateTo]);

  useEffect(updateOnLogin, [token, updateOnLogin]);

  return (
    !['', false, null, undefined].includes(token.token) ?
    <Box sx={{display: 'flex'}}>
      <CircularProgress />
    </Box> :
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{bgcolor: 'secondary.main'}}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Typography
            component="h1"
            variant="h4"
            sx={{color: 'secondary.main'}}>
            <strong>Currency Converter</strong>
          </Typography>
          <Box
            component="form"
            onSubmit={handleLogin}
            noValidate={false}
            sx={{mt: 1}}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              value={username}
              onChange={handleUsername}
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              value={password}
              onChange={handlePassword}
            />
            <LoadingButton
              type="submit"
              fullWidth
              loading={loadingButton}
              loadingPosition="start"
              variant="contained"
              sx={{mt: 3, mb: 2}}
            >
              Sign In
            </LoadingButton>
          </Box>
        </Box>
        <Copyright sx={{mt: 8, mb: 4}} />
        <Snackbar
          autoHideDuration={6000}
          anchorOrigin={{vertical, horizontal}}
          open={openSnackbar}
          onClose={handleSnackbarClose}
          key={vertical + horizontal}
        >
          <Alert
            onClose={handleSnackbarClose}
            severity="error"
            sx={{width: '100%'}}>
            {msgSnackbar}
          </Alert>
        </Snackbar>
      </Container>
    </ThemeProvider>
  );
};
