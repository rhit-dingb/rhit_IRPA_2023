import "../chatBot.css";
import React from "react";
import { react, useEffect, useState, useRef } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import * as XLSX from 'xlsx';
import {CUSTOM_BACKEND_API_STRING, DataType, TOKEN_KEY} from "../../constants/constants"
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';

import FolderIcon from '@mui/icons-material/Folder';
import { FixedSizeList, ListChildComponentProps } from 'react-window';
import Avatar from '@mui/material/Avatar';

import ListItemAvatar from '@mui/material/ListItemAvatar';
import Button from '@mui/material/Button';
import {Navbar} from "../Navbar"
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';

import CircularProgress from '@mui/material/CircularProgress';
import { green } from '@mui/material/colors';
import DeleteIcon from '@mui/icons-material/Delete';
import IconButton from '@mui/material/IconButton';

import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import Alert from '@mui/material/Alert';
import { checkResponse } from "../../functions/functions";

function UploadData(props) {
  const uploadDataRef = useRef(null)
  const uploadDefinitionRef = useRef(null)

  // const [dataToUpload, setDataToUpload] = useState({})

  const [dataList, setDataList] = useState([])
  const [definitionDataAvailable,  setDefinition] = useState("")

  // This state looks something like this {"enrollment": "general"}
  const [sectionAndSubSections, setSectionAndSubSections] = useState({})

  //0th index is the defintion list item, the annual data items indexed starting at 1. 
  const [selectedIndex, setSelectedIndex] = useState(1);

  const [notificationMessage, setNotificationMessage] = useState("")
  const [showNotification, setShowNotification] = useState(false)
  const [notificationBannerColor, setNotificationColor ] = useState("error")
  const [isUploading, setIsUploading] = useState(false)

 


  useEffect(() => {
    fetchAnnualData()
    fetchDefinition()
  }, []);


  const fetchAnnualData = ()=>{
    fetchAvailableData(DataType.ANNUAL).then((dataAvailable)=>{
    
      setDataList(dataAvailable)
    })
  }

  const fetchDefinition = () =>{
  
    fetchAvailableData(DataType.DEFINITION).then((definitionAvailable) => {
      if (definitionAvailable.length > 0 ){
        setDefinition(definitionAvailable[0])
      } else{
        setDefinition("")
      }
        
    })
  }


  useEffect(()=> {
    if (dataList.length>0){
      let dataName = dataList[selectedIndex-1]
    
      fetchSectionSubsectionForData(dataName).then(()=>{
        console.log(sectionAndSubSections)
      }) 
    }
   
  }, [dataList])


  // Should probably refactor these api calls to be a general function. 
  const fetchAvailableData = ((type)=> {
      return fetch(`${CUSTOM_BACKEND_API_STRING}/api/get_available_data/${type}`, {
        method: 'GET',
      }).then((response) => response.json())
      .then((data) => {
          // console.log("GOT DATA BACK")
          if ("data" in data){
              let dataAvailable = data["data"]
              
              return dataAvailable
          } else{
            // console.log("NO DATA AVAILABLE")
            return []
          }
        
      }).catch((err)=>{
          console.error(err)
          return []
      })
  })


  const fetchSectionSubsectionForData = (async (dataName) => {
    let body = {"dataName": dataName}
    //With async function we can replace .then and .catch, but they basically do the same thing
    try {
      const response = await fetch(CUSTOM_BACKEND_API_STRING + '/api/get_section_and_subsection_for_data', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "http://localhost:3000",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type"
        },
      });
      const data = await response.json();
      if ("data" in data) {
        let sectionAndSubSections = data["data"];
        setSectionAndSubSections(sectionAndSubSections);
       
      }
    } catch (err) {
      console.log(err);
    }
  })

  // useEffect(() => {
  //    alert(errorMessage)
  // }, [showErrorMessage, errorMessage]);
  

  const validateAnnualFileName = (fileName) => {
    const errorMessage = "Input file for annual data should be of the format: someName_start year_end year"
    let tokens = fileName.split("_")
    
    if (tokens.length != 3) {
      displayErrorMessage(errorMessage)
      return false
    }

    let yearFrom = tokens[1]
    let yearTo = tokens[2]
    yearFrom = parseInt(yearFrom)
    yearTo = parseInt(yearTo)
    if (yearFrom === NaN || yearTo === NaN) {
      displayErrorMessage(errorMessage)
      return false
    }

    return true 
    // return [yearFrom, yearTo]
  }


  const validateDefinitionFileName = (fileName) => {
    const definitionKey = "definition"
    const errorMessage = "Input file for annual data should be of the format: someName_definition"
    let tokens = fileName.split("_")
    if (tokens.length > 2) {
      displayErrorMessage(errorMessage)
      return false
    }
    for (let token of tokens) {
      if (token.toLowerCase() == definitionKey){
        return true
      }
    }

    displayErrorMessage(errorMessage)
    return false
  }
  
  

  const handleUploadDefinition = (event) => {
    let file = event.target.files[0]
    // let fileName = file.name
    uploadDefinitionRef.current.value = "" 
    // let res = validateDefinitionFileName(fileName)
    // let body = {"dataName": fileName, "type": DataType.DEFINITION}
    // handleUpload(file, body).then(()=> {
    //   console.log("RETRIEVING DEFINITION DATA AVAILABLE")
    //   fetchDefinition()
    // })
    validateAndUpload(file, validateDefinitionFileName, fetchDefinition)
    
  }

  const validateAndUpload = (file, validationFunc, updateFunc)=>{
    let fileName = file.name
    //Remove file extension
    fileName = fileName.slice(0, fileName.lastIndexOf("."));
    let res = validationFunc(fileName)
    let body = {"dataName": fileName}
    if (res){
      console.log("UPLOAD FILE")
      handleUpload(file, body).then(()=> {
        console.log("RETRIEVING DATA AVAILABLE")
        updateFunc()
      })
    } 
  } 

  const handleUploadAnnualData = (event) => {
    let file = event.target.files[0]
    uploadDataRef.current.value = ""
    validateAndUpload(file, validateAnnualFileName, fetchAnnualData)
      
  }

  const handleUpload = (file, body) => {
        // let file = event.target.files[0]
        const reader = new FileReader();
        reader.readAsArrayBuffer(file)
        // With async function, we can use await, along with try and catch instead of using then.
        return new Promise((resolve, reject)=> {
          reader.onload = () => {
            const result = reader.result
            const workbook = XLSX.read(result, { type: 'array' });

            let jsonData = {}
            for (let sheetName of workbook.SheetNames) {
                const sheet = workbook.Sheets[sheetName];
                jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
            }

            body["data"] = jsonData
            console.log("BODY")
            console.log(JSON.stringify(jsonData))
            setIsUploading(true)
            const infoMessage = "File is uploading...."
            displayInfoMessage(infoMessage)
            
            fetch(CUSTOM_BACKEND_API_STRING + '/api/upload_data', {
                method: 'POST',
                body: JSON.stringify(body),
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "http://localhost:3000",
                  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                  "Access-Control-Allow-Headers": "Content-Type"
                },
              }).then((result_1) => {
                  result_1.json().then((data) => {
                    setIsUploading(false);
                    let resultJson = data;
                    if (!result_1.ok) {
                      displayErrorMessage(resultJson["detail"])
                    }else{
                      let uploadedAs = ""
                      if ("uploadedAs" in resultJson){
                        let fileName = resultJson["uploadedAs"]
                        uploadedAs = `as ${fileName}`
                      }
                      
                      displaySuccessMessage(`File uploaded successfully ${uploadedAs}`)
                      console.log("UPLOAD DONE")
                    }

                    resolve()
                }).catch((err) =>{
                      console.error(err);
                      displayErrorMessage(err)
                      reject()
                  })
                }).catch((err) => {
                  console.log(err);
                  setIsUploading(false);
                  displayErrorMessage(err)
                  reject()
                })
              }
            })
    };
  


    const displayErrorMessage = (message)=>{
      displayMessage(message, "error")
    }

    const displayInfoMessage= (message) =>{
      displayMessage(message, "info")
    }

    const displaySuccessMessage = (message)=> {
      displayMessage(message, "success")
    }

    const displayMessage = (message, color) => {
      setShowNotification(false)
      setNotificationMessage(message);
      setShowNotification(true);
      setNotificationColor(color)
    }


  
    const handleDataClick = (event, index)=>{
        let dataName = ""
        //0th index is taken by definition
        if (index == 0){
          dataName = definitionDataAvailable
        } else {
          dataName = dataList[index-1]
        }
       
        setSectionAndSubSections([])
        //0th index is taken by definition
        setSelectedIndex(index)
        fetchSectionSubsectionForData(dataName)
    }

    const handleDeleteData = (event, index)=>{
      let selectedDefinition = index == 0
      let dataName = ""
      let updateFunc = ()=>{}
      if (selectedDefinition) {
          dataName = definitionDataAvailable
          updateFunc = fetchDefinition
      } else {
          dataName = dataList[index-1]
          updateFunc = fetchAnnualData
      }

      deleteData(dataName, updateFunc)
    }


    const deleteData = (dataName, updateFunc)=>{
      let body ={ "dataName": dataName}
      fetch(CUSTOM_BACKEND_API_STRING + '/api/delete_data', {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
          "Authorization": localStorage.getItem(TOKEN_KEY)
        },
      }).then((response)=>{
          const successCallback = (jsonData)=>{
            displaySuccessMessage("Deletion successful")
            console.log("UPDATE after delete")
            updateFunc()
          }

          checkResponse(response, displayErrorMessage, successCallback, props.history)
          
      }).catch((err)=>{
        displayErrorMessage(err)
      })
    }


    const createElementForSectionAndSubSection = ()=> {
      let keyToValueArr = Object.entries(sectionAndSubSections)
      // Sort the sections alphabetically
      keyToValueArr = keyToValueArr.sort()
      return keyToValueArr.map(([key, value]) => {
        return (
          <Accordion key = {key}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              className="panel1a-header"
            >
            <Typography>{key}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              {
                value.map((val, index)=>{
                  return (<Typography key ={index}>
                    {val} 
                  </Typography>)
                })
              }
            </AccordionDetails>
          </Accordion>)
      })
    }
      


  
    return (
        
        <div style={{height:"100vh"}}>
            <Navbar/>
            <Box
            sx={{ width: '80%', margin: "auto", marginTop:"3%"}}
            >
          
            {showNotification && <Alert severity={notificationBannerColor} onClose={() => {setShowNotification(false)}}>{notificationMessage}</Alert>}
            <Card variant="outlined"  sx={{padding:"10px",  minHeight: "550px"}}>
            <Grid container>
              <Grid item md={3} xs={12}  bgcolor="primary" sx={{ minHeight: "550px", backgroundColor: "#E7EBF0"
                   }}>
                <Box sx={{ minHeight: "100px", padding:"2%"}}>
                <h5>Uploaded Definition</h5>
                {definitionDataAvailable && <List  sx={{
                    overflow: 'auto',
                }}> 
                  <ListItem  component="div" 
                      disablePadding
                      sx ={{padding:"3%"}}
                      secondaryAction={
                        <IconButton edge="end" aria-label="delete" onClick={(e)=> handleDeleteData(e, 0 )}>
                          <DeleteIcon />
                        </IconButton>
                      }
                    >
                    <ListItemAvatar>
                    <Avatar>
                    <FolderIcon />
                    </Avatar>
                  </ListItemAvatar>
                    <ListItemButton
                    selected={selectedIndex === 0}
                    onClick={(event) => handleDataClick(event, 0)}>
                    <ListItemText primary={`${definitionDataAvailable}`} className ="listItemText" /> 
                    </ListItemButton> 
                  </ListItem>
                </List>}

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
                  
                  <input hidden ref={uploadDefinitionRef}  type="file" accept=".xlsx" onChange={(e) => handleUploadDefinition(e)} />
                </Button>
                
                </Box> 
                <Divider variant="middle" />
  
                <h5>Uploaded Annual Data</h5>
                <List  sx={{
                    overflow: 'auto',
                    maxHeight: "450px"
                }}> 

                  {dataList.map((item, index)=>{
                    return ( 
                    <div  key={index}>
                    <ListItem  component="div" 
                      disablePadding
                      sx ={{padding:"3%"}}
                      secondaryAction={
                        <IconButton edge="end" aria-label="delete" onClick={(e)=> handleDeleteData(e, index+1 )}>
                          <DeleteIcon />
                        </IconButton>
                      }
                    >
                    <ListItemAvatar>
                    <Avatar>
                    <FolderIcon />
                    </Avatar>
                  </ListItemAvatar>
                    <ListItemButton
                    selected={selectedIndex === index+1}
                    onClick={(event) => handleDataClick(event, index+1)}>
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
                  <input hidden ref={uploadDataRef}  type="file" accept=".xlsx" onChange={(e) => handleUploadAnnualData(e)} />
                </Button>
              </Grid>

              <Grid item md={9} xs={12} sx={{ maxHeight: "500px",
                   }}>
                  <Card variant="outlined" sx={{ maxHeight: "100%",
                    overflowY:"auto",
                   }}>

                  <CardContent>
                    <Typography sx={{ fontSize: 25 }} color="text.primary" gutterBottom>
                      Knowledge
                    </Typography>
                    {createElementForSectionAndSubSection()}
                    </CardContent>
                  </Card>
              </Grid>
            </Grid>
            </Card>
            </Box>
        </div>
    )
}




export default UploadData
