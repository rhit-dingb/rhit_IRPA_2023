import { ChatbotResponseType, RESPONSE_TYPE_KEY, CHATBOT_TEXT_MESSAGE_KEY ,CHATBOT_CUSTOM_MESSAGE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import { AccordionList } from "./AccordionList"


function ChatbotResponse({recipientId, keyToUse, jsonResponse}) {
    const recipient_id = recipientId
    let responseData = jsonResponse
    let type = null

    const initialize = ()=>{
        determineResponseType(jsonResponse)
        return parseToUI(jsonResponse)
    }

    const determineResponseType = (jsonResponse)=>{
        if (CHATBOT_CUSTOM_MESSAGE_KEY in jsonResponse){
            let customData = jsonResponse[CHATBOT_CUSTOM_MESSAGE_KEY]
            if(RESPONSE_TYPE_KEY in customData) {
                let responseType = customData[RESPONSE_TYPE_KEY ]
                responseData = customData
                switch(responseType) {
                    case "accordion list":
                      type = ChatbotResponseType.ACCORDION_LIST
                      break;
    
                    default:
                        type = ChatbotResponse.NORMAL_MESSAGE
                        return
                }
            } else {
                type  = ChatbotResponseType.NORMAL_MESSAGE
            }
        } else {
            type  = ChatbotResponseType.NORMAL_MESSAGE
        }
    }

    const parseToUI = (jsonResponse) => {
        console.log(type)
        switch(type) {
            case ChatbotResponseType.ACCORDION_LIST:
              return (<AccordionList jsonResponse = {responseData}/>)
            default:
                let message = null
                if("custom" in jsonResponse){
                    let customData = jsonResponse["custom"]
                    message = customData[CHATBOT_TEXT_MESSAGE_KEY ]
                } else{
                    message = jsonResponse[CHATBOT_TEXT_MESSAGE_KEY ]
                }

                // console.log(jsonResponse)
                // console.log("MESSAGE"+message)
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