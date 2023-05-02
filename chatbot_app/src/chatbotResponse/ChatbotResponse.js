import { ChatbotResponseType, RESPONSE_TYPE_KEY, CHATBOT_TEXT_MESSAGE_KEY ,CHATBOT_CUSTOM_MESSAGE_KEY, CHATBOT_IMAGE_MESSAGE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import { AccordionList } from "./AccordionList"
import { TextAnswer } from "./TextAnswer";


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
                let responseType = customData[RESPONSE_TYPE_KEY]
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
        // console.log(type)
        // console.log(jsonResponse)
        switch(type) {
            case ChatbotResponseType.ACCORDION_LIST:
              return (<AccordionList jsonResponse = {responseData}/>)
            default:
                // Default handle the input data if not custom response type is specified.
                //Used to parse text, and image and can be used to parse other type of ui supported.
                let message = null
                let source = null
                if(CHATBOT_CUSTOM_MESSAGE_KEY in jsonResponse){
                    let customData = jsonResponse["custom"]
                    message = customData[CHATBOT_TEXT_MESSAGE_KEY ]
                    source = customData["source"]
                } else if (CHATBOT_TEXT_MESSAGE_KEY in jsonResponse) {
                    message = jsonResponse[CHATBOT_TEXT_MESSAGE_KEY]
                } else if (CHATBOT_IMAGE_MESSAGE_KEY in jsonResponse) {
                    message = jsonResponse[CHATBOT_IMAGE_MESSAGE_KEY]
                }
                
                let answer = message
                console.log(jsonResponse)
                if (answer == null) {
                    return null
                }
                answer = answer.charAt(0).toUpperCase() + message.slice(1)
                return  (<TextAnswer isAdmin={false} answer={answer} questionId={null} feedback={null} source={source} />)
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