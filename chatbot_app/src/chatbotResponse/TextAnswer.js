

import React from "react";
import { react, useEffect, useState, useRef } from "react";
import Divider from '@mui/material/Divider';
import ThumbUpAltOutlinedIcon from '@mui/icons-material/ThumbUpAltOutlined';
import ThumbDownOutlinedIcon from '@mui/icons-material/ThumbDownOutlined';
import { BiBot, BiUser } from "react-icons/bi";
import IconButton from '@mui/material/IconButton';
import {CUSTOM_BACKEND_API_STRING, TOKEN_KEY} from "../constants/constants"

export function TextAnswer({isAdmin, questionId, answer, feedback}) {
    // console.log(questionId)
    // console.log(answer)

    const [currentFeedback, setCurrentFeedback] = useState(null)
 
    useEffect(() => {
        setCurrentFeedback(feedback)
        // console.log("_____________________________")
        // console.log(answer)
        // console.log(feedback)
        // console.log("_____________________________")
    }, [feedback]);


    const sendFeedback= (feedback)=>{
        let body = {"isAdmin": isAdmin, "questionId": questionId, "chatbotAnswer": answer, "feedback":feedback}
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


    return ( 
        <div>
            {isAdmin &&(<div>
            <p>
            <span style={{marginRight:20}}>{answer}</span>
            <IconButton isize="small" onClick={(e)=>{sendFeedback("correct")}}><ThumbUpAltOutlinedIcon fontSize="small" color={currentFeedback==="correct"? "primary" :""} /></IconButton>
            <IconButton size="small" onClick={(e)=>{sendFeedback("incorrect")}}>  <ThumbDownOutlinedIcon fontSize="small" color={currentFeedback==="incorrect"? "primary" :""}/></IconButton>
            </p>
            <Divider/>
            </div>)}

            {!isAdmin &&
            (<div>
                <div className="msgalignstart">
                    <BiBot className="botIcon" />
                    <h5 className="botmsg">{answer}</h5>
                </div> 
            </div>)
            }
        </div>
       
    )
}
