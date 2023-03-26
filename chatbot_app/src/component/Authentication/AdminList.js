import { React, useEffect, useState, useRef} from "react";
import { Navbar } from "../Navbar";
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';

import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { checkResponse, getCurrentUser } from "../../functions/functions";
import { stringify } from "uuid";
import { TOKEN_KEY } from "../../constants/constants";
import {CUSTOM_BACKEND_API_STRING} from "../../constants/constants"
import SecurityIcon from '@mui/icons-material/Security';
import SettingsApplicationsIcon from '@mui/icons-material/SettingsApplications';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';


function AdminList(props) {

    const [adminList, setAdminList] = useState([])
    const [currentUserData, setCurrentUserData] = useState({})
    const [showAddAdminForm, setShowAddAdminForm] = useState(false)
    const newAdminUsernameInputRef = useRef()

    useEffect(() => {
        fetchAdminList()
        getCurrentUser(localStorage.getItem(TOKEN_KEY), props.history, (userData)=>{
            console.log(userData)
            setCurrentUserData(userData)
        })
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
            return ( 
                <TableRow
                key={item.username}
                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                <TableCell align="center"  component="th" scope="row">
                    {item.username}
                </TableCell>
                <TableCell align="center">{item.role}</TableCell>
                {currentUserData.username != item.username
                    && <TableCell align="center">
                        <Button disabled ={currentUserData.role=="root"? false: true} variant="outlined" color="error" onClick={(e)=>{deleteAdmin(item.username)}}>Delete User</Button>
                        </TableCell>
                }
                </TableRow>)
        })

        // adminList.map((row) => (
        //     <TableRow
        //     key={row.name}
        //     sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
        //     >
        //     <TableCell component="th" scope="row">
        //         {row.name}
        //     </TableCell>
        //     <TableCell align="right">{row.calories}</TableCell>
        //     <TableCell align="right">{row.fat}</TableCell>
        //     <TableCell align="right">{row.carbs}</TableCell>
        //     <TableCell align="right">{row.protein}</TableCell>
        //     </TableRow>
        // ))
    }

    const deleteAdmin = (username)=>{
        let body ={ "username": username}
        return fetch(`${CUSTOM_BACKEND_API_STRING}/delete_user`, {
            method: 'DELETE',
            headers: {
                "Content-Type": "application/json",
                "Authorization": localStorage.getItem(TOKEN_KEY)
              },
            body:JSON.stringify(body)
        }).then((response) =>{
            checkResponse(response, (stringifyData)=>{}, 
            (stringifyData)=>{
               console.log("DELETION SUCCESS")
               fetchAdminList()
            }, props.history)
        })
    }
      

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
      };

    return(
        <div style = {{height:"100vh"}}>
            <Navbar/>
            {/* <Box sx={{ width: '80%', margin: "auto", marginTop:"3%", backgroundColor: "#E7EBF0", minHeight: "80%"}}>
                <h4>Administrator List</h4>
                <List>
                    {generateListElem()}
                </List>
            </Box> */}
            
            <Box sx={{ width: '80%', margin: "auto", padding:2, marginTop:"3%", backgroundColor: "#E7EBF0", minHeight: "80%", maxHeight: "80%", overflowY:"scroll",overflowX:"hidden" }}>
                <h2>Administrator List</h2>
                <TableContainer component={Paper} sx={{minHeight: "80%", }}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                        <TableRow>
                            <TableCell  align="center"><AccountCircleIcon/> Username</TableCell>
                            <TableCell align="center"><SecurityIcon/> Role</TableCell>
                           <TableCell align="center"><SettingsApplicationsIcon/> Action</TableCell>
                        </TableRow>
                        </TableHead>
                        <TableBody>
                        {generateListElem()}
                       
                        </TableBody>
                    </Table>
                    </TableContainer>

                    <Modal
                        open={showAddAdminForm}
                        onClose={()=>{}}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <Box sx={style}>
                            <Typography id="modal-modal-title" variant="h6" component="h2">
                                Create new admin
                            </Typography>
                            <br/>
                            {/* <Typography >
                            Rose-Hulman Username 
                            </Typography> */}
                            <TextField id="filled-basic" label="Rose-Hulman Username" variant="filled" ref={newAdminUsernameInputRef} />
                            <br/>
                            <br/>

                            <Button variant="outlined" color="info" onClick={(e)=>{}} sx={{marginRight:2}}>Submit</Button>
                            <Button variant="outlined" color="error" onClick={(e)=>{setShowAddAdminForm(false)}}>Cancel</Button>
                        </Box>
                    </Modal>

                    <br/>
                    <Button disabled ={currentUserData.role=="root"? false: true} variant="contained" color="info" onClick={(e)=>{setShowAddAdminForm(true)}}>Add Admin</Button>
                </Box>
        </div>
    )

 
      

}

export default AdminList;