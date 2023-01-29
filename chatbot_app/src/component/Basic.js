import "./chatBot.css";
import React from "react";
import react, { useEffect, useState } from "react";
import { IoMdSend } from "react-icons/io";
import { BiBot, BiUser } from "react-icons/bi";
import { RASA_API_STRING, RESPONSE_TYPE_KEY, GET_AVAILABLE_OPTIONS_MESSAGE, CHATBOT_TEXT_MESSAGE_KEY } from "../constants/constants";
import Box from '@mui/material/Box';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import YearSelect from "./YearSelect"
import ChatbotResponse from "../chatbotResponse/ChatbotResponse"
import { v4 as uuidv4 } from 'uuid';
import CircleIcon from '@mui/icons-material/Circle';

function Basic() {
 
  const [chat, setChat] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const [botTyping, setbotTyping] = useState(false);
  const [conversationId, setConversationId] = useState(uuidv4())

  useEffect(()=>{
   
    if (chat.length ==0) {
      let body = { }
     
      body[CHATBOT_TEXT_MESSAGE_KEY] =  "Hi! I am a chatbot for the IPRA office, I can help you answer various questions related to Rose-Hulman."
      const request_temp = { sender: "bot", sender_id: "test", jsonData:  body }
      setbotTyping(true)
      setChat([...chat, ...[request_temp]])
      rasaAPI(conversationId, GET_AVAILABLE_OPTIONS_MESSAGE)
      
    }
   

  },[])

  useEffect(() => {
    //console.log("called");
    const objDiv = document.getElementById("messageArea");
    objDiv.scrollTop = objDiv.scrollHeight;
  }, [chat]);

  const handleSubmit = (evt) => {
    evt.preventDefault();
    const name = "user1";
    const request_temp = { sender: "user", sender_id: name, msg: inputMessage };

    if (inputMessage !== "") {
      setChat((chat) => [...chat, request_temp]);
      setbotTyping(true);
      setInputMessage("");
      rasaAPI(conversationId, inputMessage);
    } else {
      window.alert("Please enter valid message");
    }
  };

  const rasaAPI = async function handleClick(conversationId, msg) {
    //chatData.push({sender : "user", sender_id : name, msg : msg});
    console.log(chat);
    await fetch(
      `${RASA_API_STRING}/webhooks/rest/webhook`,
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          charset: "UTF-8",
        },
        credentials: "same-origin",
        mode: "cors",
        body: JSON.stringify({ sender: conversationId, message: msg }),
      }
    )
      .then((response) => response.json())
      .then((response) => {
        if (response) {
          
          // const temp = response[0];
          console.log("RESPONSE RECEIVED")
          console.log(response)
          let messages = []
          for (let r of response) {
              const recipient_id = r["recipient_id"];
              //Expect the backend return the following json
              // {custom:{text:"", ...other stuff }}
              const response_temp = {
                sender: "bot",
                recipient_id: recipient_id,
                jsonData: r
              };

            
              messages.push(response_temp)
          }
          
          setbotTyping(false);

          setChat((chat) => [...chat, ... messages]);
          // scrollBottom();
        }
      });
  };



  const styleChatbotBody  = {
    // maxWidth: "100rem",
    width: "100%",
    // width: "200rem",
    border: "1px solid black",
    paddingLeft: "0px",
    paddingRight: "0px",
    borderRadius: "30px",
    boxShadow: "0 16px 20px 0 rgba(0,0,0,0.4)",
  };


  const styleHeader = {
    height: "3.5rem",
    borderBottom: "1px solid black",
    borderRadius: "30px 30px 0px 0px",
    backgroundColor: "#800000",
    
  };
  const styleFooter = {
    // maxWidth: "80%",
    borderTop: "1px solid black",
    borderRadius: "0px 0px 30px 30px",
    backgroundColor: "#800000",
  };

  const styleBody = {
    paddingTop: "10px",
    height: "32rem",
    overflowY: "a",
    overflowX: "hidden",
  };

  return (
    <div>
      {/* <button onClick={()=>rasaAPI("shreyas","hi")}>Try this</button> */}

      {/* <div className="container"> */}
      <Box
      sx={{
        margin: "auto",
        width: "95%",
        height: "88%"
      }}>
        <div className="row justify-content-center">
          <div className="card" style={styleChatbotBody}>
            <div className="cardHeader text-white" style={styleHeader}>
            <div id="chatHeader">
            <YearSelect convId ={conversationId}/>
            <Box>
            {/* <h1 style={{margin:"auto" }}></h1> */}
              {/* {botTyping ? <h6>Bot Typing....</h6> : null}    */}
            </Box>
            </div>
            </div>

            {/*  */}
            <div className="cardBody" id="messageArea" style={styleBody}>
              <Box>
                {chat.map((user, key) => (
                  <div key={key}>
                    {user.sender === "bot" ? (
                      
                      <ChatbotResponse recipientId = {user.recipient_id} keyToUse ={key} jsonResponse = {user.jsonData}/>
                    ) : (
                      <div className="msgalignend">
                        <h5 className="usermsg">{user.msg}</h5>
                        <BiUser className="userIcon" />
                      </div>
                    )}
                  </div>
                ))}

                {botTyping &&
                <div className="msgalignstart" >
                  <BiBot className="botIcon" />
                  <h5 className="botmsg saving" >
                    Bot is typing <span>
                    <CircleIcon sx={{fontSize: 10, color:"black"}}/>
                    </span>
                    <span>
                    <CircleIcon sx={{fontSize: 10, color:"black"}}/>
                    </span>

                    <span>
                    <CircleIcon sx={{fontSize: 10, color:"black"}}/>
                    </span>
                    {/* <span class ="dot">.</span><span>.</span><span>.</span>
                  */}
                  </h5>
                  {/* <h5 className="botmsg loading" style={{}}>Bot is thinking............</h5> */}
                  
                </div>}

              </Box>
            </div>

            
            <div className="cardFooter text-white" style={styleFooter}>
              {/* <div className="row"> */}
                <form style={{ display: "flex" }} onSubmit={handleSubmit}>
                  <div className="col-11" style={{ paddingRight: "0px"}}>
                    <input
                      onChange={(e) => setInputMessage(e.target.value)}
                      value={inputMessage}
                      type="text"
                      className="msginp"
                    ></input>
                  </div>
                  <div className="col-1 cola">
                    <button type="submit" className="circleBtn">
                      <IoMdSend className="sendBtn" />
                    </button>
                  </div>
                </form>
              {/* </div> */}
            </div>
          </div>
        </div>
      {/* </div> */}
      </Box>
    </div>
  );



}



export default Basic;
