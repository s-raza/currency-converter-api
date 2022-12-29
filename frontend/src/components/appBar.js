import React from 'react';
import {AppBar, Toolbar, Typography, Box} from '@mui/material';

const TopBar = ({loginButton}) => {
  return (
    <Box sx={{flexGrow: 1}}>
      <AppBar position="static" >
        <Toolbar variant="dense">
          <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
            Currency Converter
          </Typography>
          {loginButton}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default TopBar;
