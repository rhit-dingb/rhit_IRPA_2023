

import React from "react";
import { react, useEffect, useState, useRef } from "react";
import Divider from '@mui/material/Divider';
import ThumbUpAltOutlinedIcon from '@mui/icons-material/ThumbUpAltOutlined';
import ThumbDownOutlinedIcon from '@mui/icons-material/ThumbDownOutlined';
import { BiBot, BiUser } from "react-icons/bi";
import IconButton from '@mui/material/IconButton';
import {CUSTOM_BACKEND_API_STRING, TOKEN_KEY} from "../constants/constants"
import Stack from '@mui/material/Stack';
export function TextAnswer({isAdmin, questionId, answer, feedback, source}) {
    // console.log(questionId)
    // console.log(answer)
   
    const [currentFeedback, setCurrentFeedback] = useState(null)
 
    useEffect(() => {
        setCurrentFeedback(feedback)
    
    }, [feedback]);


    const sendFeedback= (feedback)=>{
        let body = {"isAdmin": isAdmin,"chatbotAnswer": answer, "feedback":feedback}
        if (questionId != null){
            body["questionId"] = questionId
        }

        fetch(`${CUSTOM_BACKEND_API_STRING}/update_answer_feedback`, 
            {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(body)
            }
        ).then((response)=>{
            console.log(response)
            response.json().then((data)=>{
                console.log(data)
                let success = data["success"]
                if (success == true) {
                    setCurrentFeedback(feedback)
                   
                }
            })
        })
    }


    const renderThumbsUpAndDown =()=> {
     
        if(source) {
            return ( 
            <Stack  direction="row" >
            <IconButton size="small" onClick={(e)=>{sendFeedback("correct")}}><ThumbUpAltOutlinedIcon fontSize="small" color={currentFeedback==="correct"? "primary" :""} /></IconButton>
            <IconButton size="small" onClick={(e)=>{sendFeedback("incorrect")}}>  <ThumbDownOutlinedIcon fontSize="small" color={currentFeedback==="incorrect"? "primary" :""}/></IconButton>
            </Stack>
            )
        } else{
            return null
        }
    }


    return ( 
        <div>
            {isAdmin &&(<div>
            <Stack justifyContent={"center"} spacing={2} direction="row" >
                <p>
                    {answer} 
                </p>
                {renderThumbsUpAndDown()} 
            
            </Stack>
            <Divider/>
            </div>)}

            {!isAdmin &&
            (
                <div className="msgalignstart">
               
                <BiBot className="botIcon" />
                    <Stack className="botmsg" spacing={2} direction="row" >
                        <h5 >{answer} </h5>
                        <div>
                      
                        {/* {renderThumbsUpAndDown()} */}
                       
                        </div>
                    </Stack>
                </div> 
            )
            }
        </div>
       
    )
}
