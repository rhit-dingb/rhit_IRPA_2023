import "../chatBot.css";
import React from "react";
import react, { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import * as XLSX from 'xlsx';
import {CUSTOM_BACKEND_API_STRING} from "../../constants/constants"
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';

import FolderIcon from '@mui/icons-material/Folder';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import Avatar from '@mui/material/Avatar';

import ListItemAvatar from '@mui/material/ListItemAvatar';
import Card from '@mui/material/Card';
import Button from '@mui/material/Button';
import {Navbar} from "../Navbar"
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';

import CircularProgress from '@mui/material/CircularProgress';
import { green } from '@mui/material/colors';

function UploadData() {

  const [dataToUpload, setDataToUpload] = useState({})
  const [cdsDataList, setCdsDataList] = useState([])
  const [cdsDefinitionData,  setCdsDefinition] = useState("")
  const [selectedIndex, setSelectedIndex] = useState(0);

  const [errorMessage, setErrorMessage] = useState("")
  const [showErrorMessage, setShowErrorMessage] = useState(false)
  const [isUploading, setIsUploading] = useState(false)

  const fetchAvailableCdsData = (()=> {
    fetch(CUSTOM_BACKEND_API_STRING+'/api/get_all_cds_data', {
      method: 'GET',
    }).then((response) => response.json())
    .then((data) => {
          if ("data" in data){
            let cdsDataAvailable = data["data"]
          
            setCdsDataList(cdsDataAvailable)
          
          }
    });
  })
      
  useEffect(() => {
      fetchAvailableCdsData()
    }, []);

  // useEffect(() => {
  //    alert(errorMessage)
  // }, [showErrorMessage, errorMessage]);
  

  const validateCDSFileName = (fileName) => {
    const errorMessage = "Input file for CDS should be of the format: someName_start year_end year"
    let tokens = fileName.split("_")
    
    if (tokens.length != 3) {
      setErrorMessage(errorMessage)
      return []
    }

    let yearFrom = tokens[1]
    let yearTo = tokens[2]
    yearFrom = parseInt(yearFrom)
    yearTo = parseInt(yearTo)
    if (yearFrom == NaN || yearTo == NaN) {
      setErrorMessage(errorMessage)
      return []
    }

    return [yearFrom, yearTo]
  }

  const handleUpload = (event) => {
            let file = event.target.files[0]
            let fileName = file.name
            let years = validateCDSFileName(fileName)

            const reader = new FileReader();
            reader.readAsArrayBuffer(file)
            reader.onload = () => {
            const result = reader.result
            const workbook = XLSX.read(result, { type: 'array' });

            let jsonCDSData = {}
            for (let sheetName of workbook.SheetNames) {
                const sheet = workbook.Sheets[sheetName];
                jsonCDSData[sheetName] = XLSX.utils.sheet_to_json(sheet);
            }

            let body = {data: jsonCDSData, yearTo: years[0], yearFrom: years[1]}
            console.log(CUSTOM_BACKEND_API_STRING+'/api/upload_cds_data')

            setIsUploading(true)

            fetch(CUSTOM_BACKEND_API_STRING+'/api/upload_cds_data', {
                method: 'POST',
                body: JSON.stringify(body),
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "http://localhost:3000",
                  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                  "Access-Control-Allow-Headers": "Content-Type"
                },
            }).then((result)=> {
                console.log(result)
                fetchAvailableCdsData()
                setIsUploading(false)
            })
        };
    }

    const handleListItemClick = (event, index)=>{
        console.log(event)
        setSelectedIndex(index)
    }


  
    return (
        <div style={{height:"100vh"}}>
            <Navbar/>
            <Box
            sx={{ width: '80%', margin: "auto", marginTop:"3%"}}
            >

            <Card variant="outlined"  sx={{padding:"10px",  minHeight: "500px"}}>
            <Grid container>
              <Grid item md={3} xs={12}  bgcolor="primary" sx={{ minHeight: "500px", backgroundColor: "#E7EBF0"
                   }}>
        
                
                <Box sx={{ minHeight: "100px"}}>
                <h5>Uploaded CDS Definition</h5>
                
                </Box> 
                <Divider variant="middle" />
            

                <h5>Uploaded CDS Data</h5>
                <List  sx={{
                    overflow: 'auto',
                    maxHeight: "400px"
                }}> 

                  {cdsDataList.map((item, index)=>{
                    return ( 
                    <div  key={index}>
                    <ListItem  component="div">
                    <ListItemAvatar>
                    <Avatar>
                    <FolderIcon />
                    </Avatar>
                  </ListItemAvatar>
                    <ListItemButton
                    selected={selectedIndex === index}

                    onClick={(event) => handleListItemClick(event, index)}>
                    <ListItemText primary={`${item}`} className ="listItemText" />
                    </ListItemButton>
                  </ListItem>
                  </div>
                  )
                  })}

                </List>
                <Button variant="contained" component="label" sx={{margin:"2%"}} disabled={isUploading}>
                  {isUploading && (
                    <CircularProgress
                      size={24}
                      sx={{
                        color: green[500],
                        position: 'absolute',
                        top: '50%',
                        left: '50%',
                        marginTop: '-12px',
                        marginLeft: '-12px',
                      }}
                    />
                  )}
                    Upload
                  <input hidden  type="file" accept=".xlsx" onChange={(e) => handleUpload(e)} />
                </Button>
                
              </Grid>

              <Grid item md={9} xs={12} sx={{ minHeight: "500px",
                   }}>
                <div>hi</div>

              </Grid>
            </Grid>
            </Card>
            </Box>
          
        </div>
    )
}




export default UploadData
