
import React, { Component, useEffect, useState, useRef} from "react";
import { render } from "react-dom";
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import {Navbar} from "./Navbar"
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';

import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';

import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {IS_LOGGED_IN_CONSTANT} from "../constants/constants"
import { useHistory } from 'react-router-dom';
import {CUSTOM_BACKEND_API_STRING} from "../constants/constants"

function AdminLogin() {
    // const [userName, setUserName] = useState([])
    // const [] = useState("")
    const usernameRef = useRef()
    const passwordRef= useRef()
    const history = useHistory();
    const handleLogin = (e)=>{
        console.log(e)
        e.preventDefault()
        const data = new FormData(e.currentTarget);
        console.log({
          username: data.get('username'),
          password: data.get('password'),
        });

        const username = data.get('username')
        const password = data.get('password')
        // check password and username.. I'll do it here for now.
        let body = {username: username, password: password}
        fetch(CUSTOM_BACKEND_API_STRING + '/login', {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http://localhost:3000",
              "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
              "Access-Control-Allow-Headers": "Content-Type"
            },
        }).then((response) => response.json()).then((data)=>{
            let isLoggedIn = data["loggedIn"]
            // console.log(data)
            // console.log("IS LOGGED IN")
            // console.log(isLoggedIn)
            if (isLoggedIn) {
                localStorage.setItem(IS_LOGGED_IN_CONSTANT, true)
                //redirect
                history.push('/unanswered_questions');
            }
        })
        // if (username == "admin" && password =="admin123"){
        //     localStorage.setItem(IS_LOGGED_IN_CONSTANT, true)
        //     //redirect
        //     history.push('/unanswered_questions');
        // }
      
    }


    

    return(
        <div >
        {/* UI demo taken from 
        https://github.com/mui/material-ui/blob/v5.11.7/docs/data/material/getting-started/templates/sign-in/SignIn.js 
        */}
        <Navbar/>
        <Container component="main" maxWidth="xs">         
                <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
                >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <Typography component="h1" variant="h5">
                    Administrator Sign in
                </Typography>
                <Box component="form" onSubmit={handleLogin} noValidate sx={{ mt: 1 }}>
                    <TextField
                        ref = {usernameRef}
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        autoComplete="username"
                        autoFocus
                    />
                    <TextField
                    ref = {passwordRef}
                    margin="normal"
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    />
                    <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                    >
                    Sign In
                    </Button>
                </Box>
                </Box>
            </Container>
        </div>
    )
}

export default AdminLogin;