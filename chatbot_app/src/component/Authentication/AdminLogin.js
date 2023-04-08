
import React, { Component, useEffect, useState, useRef} from "react";
import { render } from "react-dom";
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import {Navbar} from "../Navbar"
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
import {IS_LOGGED_IN_CONSTANT, TOKEN_KEY} from "../../constants/constants"
import { useHistory } from 'react-router-dom';
import {CUSTOM_BACKEND_API_STRING} from "../../constants/constants"
import rose_logo from "../../rose_logo.png"
// import RoseFire from "./rosefire.min.js"
import RoseFire from "rosefire"

function AdminLogin(props) {
    // const [userName, setUserName] = useState([])
    // const [] = useState("")
  
    const history = useHistory();
    useEffect(() => {
        if (history.location.state){
            alert(history.location.state)
        }
      }, []);

    const handleLogin = (e)=>{
        console.log(e)
        e.preventDefault()
        console.log(RoseFire.Rosefire)
        let token = "14d5e015-3535-4a1e-bafc-c7aa4ac41363"
        // console.log(props.history)
        // props.history.push({pathname:'/unanswered_questions', state: "key" })
        // localStorage.setItem(IS_LOGGED_IN_CONSTANT, true)

        RoseFire.Rosefire.signIn(token, (err, rfUser) => {
			if (err) {
			  console.log("Rosefire error!", err);
			  return;
            }
            
            let roseHulmanUsername = rfUser.username
            console.log(rfUser)
            const data = new FormData();
            data.append("username", roseHulmanUsername)
            data.append("password", "placeholder")
            // let body= {"username": roseHulmanUsername, "password": "placeholder"}
            fetch(CUSTOM_BACKEND_API_STRING + '/token', {
            method: 'POST',
            body: data,
           
            }).then((response) => {
                if (!response.ok) {
                    //display error message
                    alert("Unauthorized Login")
                }else{
                    return response.json().then((data)=>{
                    
                        let token = data[TOKEN_KEY]
                        localStorage.setItem(TOKEN_KEY, token)
                        history.push({pathname:'/unanswered_questions' });
                        
                    })
                }
            })

        }) 
    }


    

    return(
        <div >
        {/* UI demo taken from 
        https://github.com/mui/material-ui/blob/v5.11.7/docs/data/material/getting-started/templates/sign-in/SignIn.js 
        */}


        {/* <Navbar/>
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
            </Container> */}
            <Container>
         
            <img style={roseLogoStyle} src={rose_logo} alt ="Rose-Hulman"/>
            <button style={roseFireLoginButton} type="button" class="btn" onClick={handleLogin}>Sign in with Rosefire</button>
            </Container>

        </div>
    )
}

const roseLogoStyle ={
    margin: "20px auto", display: "block", maxWidth: "350px"
}

const roseFireLoginButton = {
 
    display: "block",
    margin: "60px auto",
    color: "white",
    background: "#800000",
    fontSize: "1.1em",
    padding: "10px 30px",
    borderRadius: "5px"
}
export default AdminLogin;