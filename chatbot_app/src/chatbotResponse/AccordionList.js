
import { ChatbotResponseType, CHATBOT_CUSTOM_MESSAGE_KEY, RESPONSE_TYPE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import ListSubheader from '@mui/material/ListSubheader';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import InboxIcon from '@mui/icons-material/MoveToInbox';

import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import StarBorder from '@mui/icons-material/StarBorder';
import ListIcon from '@mui/icons-material/List';
import CircleIcon from '@mui/icons-material/Circle';

export function AccordionList({jsonResponse}) {
    const [expand, setExpand] = useState(false)
    let header = null
    let data = {}


    const validateData = () =>{
       
        if ("header" in jsonResponse) {
            header = jsonResponse["header"]
        }

        if ("data" in jsonResponse){
            data = jsonResponse["data"]
        }

     
    }

    validateData()

    const [expandForEach, setExpandForEach] = useState(Object.entries(data).map(([key, value], index) => {
        return false
    }))
    
    
    const setExpandAtIndex = (index)=>{
        let newArray = [...expandForEach]
        newArray[index] = !newArray[index]
        setExpandForEach(newArray)
    }

    const generateListContent= (listContent) =>{
        return listContent.map((elem, index) => {
            return (<ListItemButton key={index} sx={{ pl: 4 }}>
                <ListItemIcon>
                    <CircleIcon sx={{fontSize: 10, color:"black"}}/>
                </ListItemIcon>
                <ListItemText primary={elem} />
            </ListItemButton>)
        })
    }
    

    const generateList = () =>{
        let keyToValueArr = Object.entries(data)
        keyToValueArr = keyToValueArr.sort()
        // console.log(keyToValueArr)
        return keyToValueArr.map(([key, value], index) => {
            return (
                <div key ={key}>
                    <ListItemButton onClick={()=>{setExpandAtIndex(index)}}>
                    <ListItemIcon>
                    <ListIcon />
                    </ListItemIcon>
                    <ListItemText primary={key} />
                    {expandForEach[index] ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
                <Collapse in={expandForEach[index]} >
                    <List component="div" disablePadding>
                    {/* {console.log(value)} */}
                    {Array.isArray(value)? 
                        generateListContent(value)
                    : null}
                    </List> 
                </Collapse>
            </div>
       
            )
        })
      
    }

    return (
    <div className="msgalignstart">
        <BiBot className="botIcon" />
        <div  className="botmsg" style={{maxWidth:800, marginBottom:"1%"}}>
        <h5>{header} </h5>
        <List
            sx={{ width: '100%', maxWidth: "100%", padding: "1%", backgroundColor: "#F8F8F8"}}
            component="nav"
            aria-labelledby="nested-list-subheader"
        >
           {generateList()}
        </List>
        </div>
    </div>)
}


