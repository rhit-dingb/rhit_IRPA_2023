import "./chatBot.css";

import { react, useEffect, useState } from "react";
import { IoMdSend } from "react-icons/io";
import { BiBot, BiUser } from "react-icons/bi";
import { RASA_API_STRING } from "../constants/constants";
import Box from '@mui/material/Box';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import { GET_AVAILABLE_YEARS_END_POINT, CUSTOM_BACKEND_API_STRING} from "../constants/constants";

function YearSelect({ convId }) {
    // console.log(convId)
    const [currYearRange, setYearRange] = useState("")
    const [yearsList, setYearsList] = useState([])

    useEffect(() => {
        if (currYearRange != ""){
            sendSetYearRequest()
        }

    },[currYearRange])

    useEffect(() => {
        getAvailableYears().then((yearsAvailable)=>{
                // console.log(yearsAvailable)
                // //console.log(yearsList)
                // console.log(yearsAvailable)
                //If year is not available, set to most recent year
                if (yearsAvailable && yearsAvailable.length > 0) {
                    let mostRecentYearRange = yearsAvailable[0]
                    // console.log("MOST RECENT RANGE")
                    // console.log(mostRecentYearRange)
                    setYearRange(mostRecentYearRange)
                }
        }) 
    }, [])


    const getAvailableYears=()=>{
        return fetch(CUSTOM_BACKEND_API_STRING + GET_AVAILABLE_YEARS_END_POINT, {
            method: 'GET'
        }).then((result)=>{
            return result.json().then((data)=>{
                console.log(data)
                let yearsAvailable = data["data"]
                setYearsList(yearsAvailable)
            
                return yearsAvailable
               
            })
        }).catch((err)=>{
            console.log(err)
        })
    }   

    const getCurrentSelectedYear =()=> {
        return fetch(`${CUSTOM_BACKEND_API_STRING}/api/get_selected_year/${convId}`, {
            method: 'GET'
        }).then((result)=>{
            return result.json().then((data)=>{
                console.log(data)
                let selectedYearRange = data["selectedYear"]
             
                return selectedYearRange
            })
        }).catch((err)=>{
            console.log(err)
        })
    }

    const sendSetYearRequest=()=>{
        if (currYearRange.length<2){
            return 
        }

        let body = {"conversationId": convId, "startYear": currYearRange[0], "endYear": currYearRange[1]} 
        body = JSON.stringify(body)
        console.log(body)
        fetch(CUSTOM_BACKEND_API_STRING + "/api/change_year", {
            method: 'POST',
            body: body,
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http://localhost:3000",
              "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
              "Access-Control-Allow-Headers": "Content-Type"
            },
        }).then((result)=>{
            // console.log(result)
            // result.json().then((data)=>{
            //     console.log(data)
            // })
        }).catch((err)=>{
            console.log(err)

        })
    }


    return(
        <FormControl variant ="filled" size="small" sx={{m: 0.6,maxHeight:50, minWidth: 120, color:"black",  backgroundColor: "white" ,borderRadius: "5px" }}>
          <InputLabel >Year selected</InputLabel>
        <Select

        value={currYearRange}
        onChange={(e)=>{ setYearRange(e.target.value)}}
        label="Year selected"
        sx={{backgroundColor:"white", height:"100%" }}
    >
    {/* <MenuItem value="">
        <em>None</em>
    </MenuItem> */}
    {yearsList.map((year)=>{
        return <MenuItem value={year} key={year}>{year[0]+"-"+year[1]}</MenuItem>
    })}
    

    </Select>
    </FormControl>)

}


export default YearSelect;

