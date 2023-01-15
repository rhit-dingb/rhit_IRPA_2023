import "../chatBot.css";
import React from "react";
import { react, useEffect, useState, useRef } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import * as XLSX from 'xlsx';
import {CUSTOM_BACKEND_API_STRING, DataType} from "../../constants/constants"
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
import Snackbar from '@mui/material/Snackbar';

function UploadData() {
  const uploadCDSDataRef = useRef(null)
  const uploadCDSDefinitionRef = useRef(null)

  const [dataToUpload, setDataToUpload] = useState({})
  const [cdsDataList, setCdsDataList] = useState([])
  const [cdsDefinitionDataAvailable,  setCdsDefinition] = useState("")

  // This state looks something like this {"enrollment": "general"}
  const [sectionAndSubSections, setSectionAndSubSections] = useState({})

  //0th index is the defintion list item, the cds data items indexed starting at 1. 
  const [selectedIndex, setSelectedIndex] = useState(1);

  const [errorMessage, setErrorMessage] = useState("")
  const [showErrorMessage, setShowErrorMessage] = useState(false)
  const [isUploading, setIsUploading] = useState(false)

        
  useEffect(() => {
    fetchAvailableCdsData().then(()=>{
      // console.log("FINISHED FETCHING")
      // console.log(cdsDataList)
    })
   
  }, []);



  useEffect(()=> {
    if (cdsDataList.length>0){
      let cdsDataName = cdsDataList[selectedIndex-1]
      console.log("DAA")
      console.log(cdsDataList)
      console.log(selectedIndex)
      console.log(cdsDataName)
      fetchSectionSubsectionForCDSData(cdsDataName).then(()=>{
        console.log(sectionAndSubSections)
      }) 
    }
   
  }, [cdsDataList])


  const fetchAvailableCdsData = (()=> {
    return new Promise((resolve, reject) =>{
      fetch(CUSTOM_BACKEND_API_STRING+'/api/get_all_cds_data', {
        method: 'GET',
      }).then((response) => response.json())
      .then((data) => {
          // console.log("GOT DATA BACK")
          if ("data" in data){

              let cdsDataAvailable = data["data"]
              console.log("SETTING DATA ")
              console.log(cdsDataAvailable)
              setCdsDataList(cdsDataAvailable)
              resolve()
          } else{
            console.log("NO DATA AVAILABLE")
            resolve()
          }
        
      }).catch((err)=>{
          console.error(err)
          reject(err)
      })
    });
  })


  const fetchSectionSubsectionForCDSData = (async (cdsDataName) => {
    let body = {"cdsDataName": cdsDataName}
    try {
      const response = await fetch(CUSTOM_BACKEND_API_STRING + '/api/get_section_and_subsection_for_cds_data', {
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

  const handleUploadAnnualCDSData = (event) => {
    let file = event.target.files[0]
    let fileName = file.
    uploadCDSDataRef.current.value = ""
    let years = validateCDSFileName(fileName)
    if (years.length == 0){
      // Set and show error messages

    }
    let body = { yearTo: years[0], yearFrom: years[1], type: DataType.DEFINITION}
    handleUpload(file, body)
  }

  const handleUploadCDSDefinition = (event) => {
    let file = event.target.files[0]
    uploadCDSDefinitionRef.current.value = "" 
    let body = {type: DataType.DEFINITION}
    handleUpload(file, body)
  }

  const handleUpload = (file, body) => {
        // let file = event.target.files[0]
        const reader = new FileReader();
        reader.readAsArrayBuffer(file)
        return reader.onload = () => {
          const result = reader.result
          const workbook = XLSX.read(result, { type: 'array' });

          let jsonCDSData = {}
          for (let sheetName of workbook.SheetNames) {
              const sheet = workbook.Sheets[sheetName];
              jsonCDSData[sheetName] = XLSX.utils.sheet_to_json(sheet);
          }

          body["data"] = jsonCDSData
         
          setIsUploading(true)
          return fetch(CUSTOM_BACKEND_API_STRING+'/api/upload_cds_data', {
              method: 'POST',
              body: JSON.stringify(body),
              headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "http://localhost:3000",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
              },
          }).then(async (result)=> {
      
              fetchAvailableCdsData()
              setIsUploading(false)
              if (!result.ok) {
                // With async function, we can use await, along with try and catch instead of using then.
                try{
                  let resultJson = await result.json()
                  setErrorMessage(resultJson["detail"])
                  setShowErrorMessage(true)
                }catch(err){
                  console.error(err)
                }
              
              }
          }).catch((err) => {
              console.log(err);
              setIsUploading(false)
              setErrorMessage(err.message)
              setShowErrorMessage(true)
          });
          };
    }


    const displayErrorMessage = ()=>{

    }

    const handleCDSDataClick = (event, index)=>{

        let cdsDataName = ""
        //0th index is taken by definition
        if (index == 0){
          cdsDataName = cdsDefinitionDataAvailable
        } else {
          cdsDataName = cdsDataList[index-1]
        }
       
        setSectionAndSubSections([])
        //0th index is taken by definition
        setSelectedIndex(index)
       
        fetchSectionSubsectionForCDSData(cdsDataName)
    }


    const createElementForSectionAndSubSection = ()=> {
      let keyToValueArr = Object.entries(sectionAndSubSections)
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
          
            {showErrorMessage && <Alert severity="error" onClose={() => {setShowErrorMessage(false)}}>{errorMessage}</Alert>}
            <Card variant="outlined"  sx={{padding:"10px",  minHeight: "550px"}}>
            <Grid container>
              <Grid item md={3} xs={12}  bgcolor="primary" sx={{ minHeight: "550px", backgroundColor: "#E7EBF0"
                   }}>
                <Box sx={{ minHeight: "100px", padding:"2%"}}>
                <h5>Uploaded CDS Definition</h5>
                {cdsDefinitionDataAvailable && <List  sx={{
                    overflow: 'auto',
                }}> 
                  <ListItem  component="div" 
                      disablePadding
                      sx ={{padding:"3%"}}
                      secondaryAction={
                        <IconButton edge="end" aria-label="delete">
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
                    onClick={(event) => handleCDSDataClick(event, 0)}>
                    <ListItemText primary={`${cdsDefinitionDataAvailable}`} className ="listItemText" /> 
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
                    {/*  handleUploadCDSDefinition */}
                  <input hidden ref={uploadCDSDefinitionRef}  type="file" accept=".xlsx" onChange={(e) => handleUploadCDSDefinition(e)} />
                </Button>
                
                </Box> 
                <Divider variant="middle" />
  
                <h5>Uploaded CDS Data</h5>
                <List  sx={{
                    overflow: 'auto',
                    maxHeight: "450px"
                }}> 

                  {cdsDataList.map((item, index)=>{
                    return ( 
                    <div  key={index}>
                    <ListItem  component="div" 
                      disablePadding
                      sx ={{padding:"3%"}}
                      secondaryAction={
                        <IconButton edge="end" aria-label="delete">
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
                    onClick={(event) => handleCDSDataClick(event, index+1)}>
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
                  <input hidden ref={uploadCDSDataRef}  type="file" accept=".xlsx" onChange={(e) => handleUploadAnnualCDSData(e)} />
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
