import { ChatbotResponseType, RESPONSE_TYPE_KEY, CHATBOT_TEXT_MESSAGE_KEY ,CHATBOT_CUSTOM_MESSAGE_KEY } from "../constants/constants"
import "../component/chatBot.css"
import React, { useMemo } from "react";
import { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import { AccordionList } from "./AccordionList"
import { TextAnswer } from "./TextAnswer";
import Stack from '@mui/material/Stack';

function ChatbotResponse({recipientId, keyToUse, jsonResponse}) {
    const recipient_id = recipientId
    let responseData = jsonResponse


    const determineResponseType = (jsonResponse)=>{
        let type = null
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
                        type = ChatbotResponseType.NORMAL_MESSAGE
                        
                }
            } else {
                
                type  = ChatbotResponseType.NORMAL_MESSAGE
            }
        } else {
            type  = ChatbotResponseType.NORMAL_MESSAGE
        }

        return type
    }

    const parseToUI = (data, type) => {
        // console.log(type)
        // console.log(jsonResponse)
        let customData = null
        if(CHATBOT_CUSTOM_MESSAGE_KEY  in data){
            customData = data["custom"]
        }
       
        switch(type) {
            case ChatbotResponseType.ACCORDION_LIST:
              console.log("USE ACCORDION LIST")
              return (<AccordionList jsonResponse = {customData}/>)
            default:
                let message = null
                let source = null
                if(CHATBOT_CUSTOM_MESSAGE_KEY in data){
                    let customData = data[CHATBOT_CUSTOM_MESSAGE_KEY]
                    message = customData[CHATBOT_TEXT_MESSAGE_KEY ]
                    source = customData["source"]
                } else{
                    message = data[CHATBOT_TEXT_MESSAGE_KEY ]
                }
                
                let answer = message
                // answer = answer.charAt(0).toUpperCase() + message.slice(1)

                // // console.log("MESSAGE"+message)
                
                // // return (answer ? (<div key ={keyToUse}>
                // //     <div className="msgalignstart">
                // //         <BiBot className="botIcon" />
                // //         <h5 className="botmsg">{answer}</h5>
                // //     </div> 
                // // </div>) : null)                
               
                return  (<TextAnswer isAdmin={false} answer={answer} questionId={null} feedback={null} source={source} />)
        }
    }


    const initialize = ()=>{
        let group = []
        let currType = null
        let allUIToRender = []
      
        jsonResponse.map((customData)=>{
          
          let nextType= determineResponseType(customData)
          if (currType == nextType || currType == null){
            // Add if statement here to control which type of ui are grouped together as one message.
                group.push(customData)
                currType = nextType
          } else {
            allUIToRender.push({"type": currType, "data": group})
            currType = nextType
          }
        })
        
        allUIToRender.push({"type": currType, "data": group})
   
        return allUIToRender.map((uiData)=>{
            let group = uiData["data"]
            let type = uiData["type"] 
            console.log(type)
          
            if(type ==  ChatbotResponseType.NORMAL_MESSAGE) {
                
                return (
                <div className="msgalignstart">
                        <div>
                            {group.map((item)=>{  
                                return parseToUI(item,type)
                            })}
                        </div>
                </div>
                )
            } else{
               return( 
                <div>
                    {group.map((item)=>{
                        return parseToUI(item, type)
                    })}
                </div>
                )
            }
        })
        
    }

    const [selectedUI, setSelectedUI] = useState(initialize());
    
    useEffect(()=> {
        // determineResponseType(jsonResponse)
        // parseToUI(jsonResponse)
        // console.log(initialize())

    }, [])

    return (
        <div>
            {selectedUI}
        </div>
    )
  }


export default ChatbotResponse