import { React, useEffect, useState, useRef} from "react";
import { Navbar } from "../Navbar";
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { checkResponse } from "../../functions/functions";
import { stringify } from "uuid";
import { TOKEN_KEY } from "../../constants/constants";
import {CUSTOM_BACKEND_API_STRING} from "../../constants/constants"

function AdminList(props) {

    const [adminList, setAdminList] = useState([])

    useEffect(() => {
        fetchAdminList()
      }, []);

    const fetchAdminList=(()=>{
        return fetch(`${CUSTOM_BACKEND_API_STRING}/admins`, {
            method: 'GET',
            headers: {"Authorization": localStorage.getItem(TOKEN_KEY)}
        }).then((response) =>{
            checkResponse(response, (stringifyData)=>{}, 
            (stringifyData)=>{
               let adminList =  JSON.parse(stringifyData)
               setAdminList(adminList)
            }, props.history)
        })
         
    })
    

    const generateListElem = ()=>{
        return adminList.map((item, index)=>{
            return (<ListItem>
                <ListItemIcon>
                    <AccountCircleIcon/>
                </ListItemIcon>
                <ListItemText
                    primary={item["username"]}
                />
                </ListItem>)
        })
    }

    return(
        <div style = {{height:"100vh"}}>
            <Navbar/>
            <Box sx={{ width: '80%', margin: "auto", marginTop:"3%", backgroundColor: "#E7EBF0", minHeight: "80%"}}>
                <h4>Administrator List</h4>
                <List>
                    {generateListElem()}
                </List>
            </Box>
        </div>
    )

}

export default AdminList;