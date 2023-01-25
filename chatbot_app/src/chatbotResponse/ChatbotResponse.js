import { ChatbotResponseType, RESPONSE_TYPE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import { AccordionList } from "./AccordionList"


function ChatbotResponse({recipientId, keyToUse, jsonResponse}) {
    const recipient_id = recipientId
    let type = null
    let responseUI = null

    const initialize = ()=>{
        determineResponseType(jsonResponse)
        return parseToUI(jsonResponse)
    }

    const determineResponseType = (jsonResponse)=>{
        if(RESPONSE_TYPE_KEY in jsonResponse) {
            let responseType = jsonResponse[RESPONSE_TYPE_KEY]
            switch(responseType) {
                case "accordion list":
                  // code block
                  type = ChatbotResponseType.ACCORDION_LIST
                  break;

                default:
                    type = ChatbotResponse.NORMAL_MESSAGE
                    return
            }
        } else {
            type  = ChatbotResponseType.NORMAL_MESSAGE
        }
    }

    const parseToUI = (jsonResponse) => {
        switch(type) {
            case ChatbotResponseType.ACCORDION_LIST:
              return (<AccordionList/>)
            default:
                let message = null
                if("custom" in jsonResponse){
                    let customData = jsonResponse["custom"]
                    message = customData["text"]
                } else{
                    message = jsonResponse["text"]
                }

                return (message ? (<div key ={keyToUse}>
                    <div className="msgalignstart">
                        <BiBot className="botIcon" />
                        <h5 className="botmsg">{message}</h5>
                    </div> 
                </div>) : null) 
        }
    }

    const [selectedUI, setSelectedUI] = useState(initialize());
    
    useEffect(()=> {
        // determineResponseType(jsonResponse)
        // parseToUI(jsonResponse)

    }, [])

    return (
        <div>
            {selectedUI}
        </div>
    )
  }


export default ChatbotResponse