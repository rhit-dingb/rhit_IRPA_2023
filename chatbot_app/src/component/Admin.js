import React, { Component, useEffect, useState } from "react";
import * as ReactDOM from 'react-dom'
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
import {CUSTOM_BACKEND_API_STRING, TOKEN_KEY} from "../constants/constants"
import { Navbar } from "./Navbar";
import Stack from '@mui/material/Stack';

import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import { ListItem, List, Divider } from "@mui/material";
import { checkResponse } from "../functions/functions";
import {ChatbotAnswer, TextAnswer} from "../chatbotResponse/TextAnswer"

import CircularProgress from '@mui/material/CircularProgress';
import Typography from '@mui/material/CircularProgress';
import { green } from '@mui/material/colors';

class Question extends React.Component {
  //todo: this thing
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    //make api call here
    console.log(this.props.questionObject);
    const answerPage = (<QuestionAnswer history = {this.props.history} questionObj = {this.props.questionObject} updateFunc ={this.props.updateFunc} setSelectedQuestion = {this.props.setSelectedQuestion}/>);
    // ReactDOM.render(answerPage, document.getElementById("mainDiv"));
    this.props.setSelectedQuestion(answerPage)
  }

  render() {
    //return <button key ={this.props.questionObject.content} style={{ height:30, maxWidth:250, margin:"auto", borderColor: this.props.questionObject.is_addressed ? 'white' : 'red' }} onClick={this.handleClick}><div style={{textOverflow: "ellipsis", overflow: "hidden", whiteSpace: "nowrap"}}>{this.props.questionObject.content}</div></button>;
    return <div key ={this.props.questionObject.content} style={{ height:100, width:"100%", 
      margin:"auto", 
      border: "1px solid",
      borderColor: this.props.questionObject.is_addressed? 'green': this.props.questionObject.trained? 'blue': 'red',
      overflow: "hidden",
      height: "18%",
      padding:10,
      backgroundColor: '#E7EBF0',
      
      }} onClick={this.handleClick}>
         
        <div style={{ overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color:"black"}}>{this.props.questionObject.content}</div>
      <div style={{fontSize:11, color:"grey"}}>
      {this.props.questionObject.is_addressed? 'Answer submitted': this.props.questionObject.trained? 'Trained': ''}   
      </div>
      </div> 
      
  }
}

class QuestionAnswer extends React.Component {
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.handleTrain = this.handleTrain.bind(this);
    this.getTrainStatus = this.getTrainStatus.bind(this);
    this.showSuccessMessage = this.showSuccessMessage.bind(this);
   
    this.state = {
      question:props.questionObj.content,
      answer: props.questionObj.answer,
      notificationMessage: "",
      showNotificationMessage: false,
      alertSeverity: "success",
      chatbotAnswers: props.questionObj.chatbotAnswers,
      isTrainButtonDisabled : false, 
      intervalId : null
  
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.state.intervalId){
      clearInterval(this.state.intervalId)
      console.log("CLEAR INTERVAL")
      this.setState(prevState => ({
        
        intervalId: null
      }))
    }

    if (nextProps.questionObj !== this.props.questionObj) {
      this.setState({
         question : nextProps.questionObj.content, 
         answer: nextProps.questionObj.answer,
         chatbotAnswers: nextProps.questionObj.chatbotAnswers,
         notificationMessage: "",
         showNotificationMessage: false,
         alertSeverity: "success", 
         isTrainButtonDisabled: false
        
      });
    }
  }

  componentDidMount(){
    console.log("COMPONENT MOUNTED")
    this.getTrainStatus()
  }


  componentWillUnmount(){
  
    if (this.state.intervalId){
      clearInterval(this.state.intervalId)
      console.log("CLEAR INTERVAL")
      this.setState(prevState => ({
        
        intervalId: null
      }))
    }
  }


  getTrainStatus(){
    fetch(`${CUSTOM_BACKEND_API_STRING}/training_status`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json'}
    }).then((response)=>{
      response.json().then((data)=>{
        let status = data["isTraining"]
        if (status == false){
          if (this.state.isTrainButtonDisabled) {
            this.showSuccessMessage("Training complete!")
          } 
          this.setState(prevState => ({
            isTrainButtonDisabled : false
            
          }));
          if(this.state.intervalId) {
            clearInterval(this.state.intervalId)
            this.setState(prevState => ({
              intervalId : null
            }));



          }

        } else if(status == true){
          this.setState(prevState => ({
            isTrainButtonDisabled : true
          }));

         
        }
      
      })
    })
  }
  
  
  handleClick(e) {
    //make api call here

    e.preventDefault()
    var inputtedAnswer = document.getElementById("answerInput").value;
    if(inputtedAnswer.trim().length <= 0) {
      document.getElementById("warningText").innerHTML = "Please enter an answer";
    } else {
     
      //console.log(this.props.questionObj._id.$oid);

      let body = {
        "id": this.props.questionObj._id.$oid,
        "answer": document.getElementById("answerInput").value,
      }
      fetch(`${CUSTOM_BACKEND_API_STRING}/question_update`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 
        "Authorization": localStorage.getItem(TOKEN_KEY) 
      },
        body: JSON.stringify(body)
      })
      .then(response =>{
        let successCallback = (updateResponse)=>{
          getQuestions().then((data) => {
            this.props.updateFunc(data)
            this.showSuccessMessage("Answer updated successfully")
          });
        }
        //might refactor this
       
        checkResponse(response, this.showFailedMessage, successCallback, this.props.history)
      })
    }
  }

  showSuccessMessage = (message)=> {
    this.setState(prevState => ({
      notificationMessage: message,
      showNotificationMessage: true,
      alertSeverity: "success"
    }));
  }

  showFailedMessage = (message) => {
    this.setState(prevState => ({
      notificationMessage: message,
      showNotificationMessage: true,
      alertSeverity: "error"
    }));
  }


  handleDelete(e) {
    e.preventDefault()
    let body = {"id": this.props.questionObj._id.$oid}
    fetch(`${CUSTOM_BACKEND_API_STRING}/question_delete`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', "Authorization": localStorage.getItem(TOKEN_KEY) },
      body: JSON.stringify(body)
    })
    .then(response =>{ 
      let successCallback = (stringifiedJsonResponse) => {
          getQuestions().then((data) => {
            this.props.updateFunc(data)
            this.props.setSelectedQuestion(null)
              this.setState(prevState => ({
                notificationMessage: "Questions deleted successfully!",
                showNotificationMessage: true
            }))
          })
      }
      checkResponse(response, this.showFailedMessage, successCallback, this.props.history)
    })
  }

  handleTrain(e){
    e.preventDefault()

    let currentQuesId =this.props.questionObj._id.$oid
    fetch(`${CUSTOM_BACKEND_API_STRING}/questions/${currentQuesId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    }
    ).then(response =>{ 
      response.json().then((data)=>{
          let chatbotAnswers = data.chatbotAnswers
          let count = 0
          // for(let answer of chatbotAnswers){
          //   console.log(answer.feedback)
          //   if (answer.feedback != "" && answer.feedback != null) {
          //       count = count+1
          //   }
          // }

          // if (count<chatbotAnswers.length){
          //   this.showFailedMessage("Cannot start training for this question, not all answer are labelled")
          //   return
          // }else{
            // Start the training!!!

            this.setState(prevState => ({
              isTrainButtonDisabled: true
            }))
            this.sendTrainRequest([currentQuesId]).then((data)=>{
              console.log(data)
              // this.setState(prevState => ({
              //   isTrainButtonDisabled: false
              
              // }))
              this.showSuccessMessage("Training Signal Sent")
              let id= setInterval(this.getTrainStatus, 1000)

              this.setState(prevState => ({
                intervalId: id
              }))
             
            }).then(()=>{
              // getQuestions().then((data) => {
              //   this.props.updateFunc(data)
              // });
              this.getTrainStatus()
            })
          //}          
      })
    })
  }

  // Take in a list of question ids whose labelled answer will be used for training.
  sendTrainRequest(questionIds){
    let body = {"ids":questionIds}
    return fetch(`${CUSTOM_BACKEND_API_STRING}/train_knowledgebase`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json',
      "Authorization": localStorage.getItem(TOKEN_KEY)
      },
      body:JSON.stringify(body)
    }).then((response)=>{
       return response.json()
    })


  }



  render() {
    return (
      <Card >
      <CardContent sx={{backgroundColor:"#E7EBF0"}}>
      {/* <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          Question
        </Typography> */}
         {this.state.showNotificationMessage && <Alert severity={this.state.alertSeverity} onClose={() => { this.setState(prevState => ({
            showNotificationMessage: false
          })) 
          
          }}>{this.state.notificationMessage}</Alert>}

        <h5>Question: </h5>
        <div style={{textOverflow: "ellipsis", overflow: "scroll", marginBottom:50, overflowX: "hidden", maxHeight: 150}} >
          <h5 >{this.state.question}</h5>
        </div>
        
        <div class="form-floating">
        <h5>Chatbot Answers:</h5>
        <div style={{textOverflow: "ellipsis",overflow: "scroll", marginBottom:50, overflowX: "hidden", maxHeight: 150}} >
          {this.state.chatbotAnswers? this.state.chatbotAnswers.map((elem)=>{
            // console.log(elem)
            // return <h5>{elem.answer}</h5>
            // console.log(elem)
            
            return <TextAnswer questionId={this.props.questionObj._id.$oid} answer={elem.answer} feedback ={elem.feedback} isAdmin={true} source={elem.source}/>
          })
          : <h5>No answer from chatbot</h5>}
        </div>


        <h5>Answer</h5>
        <div id="warningText"></div>
        <textarea id="answerInput" class="form-control" value={this.state.answer || ""} onChange={e => this.setState({ answer : e.target.value })} placeholder="Provide answer here" style={{minHeight:150, maxHeight:300,minWidth: "100%",  maxWidth: "100%", textAlign: "center",  }}    />
        
      </div>
        {/* <input id="answerInput" type="text" placeholder="Enter answer text"></input> */}
      
        <Stack direction="row" spacing={2} justifyContent="center"
>
        <Button variant="contained"  onClick={this.handleClick}>
          {"Submit Answer"}
        </Button>
        <Button variant="contained" color="error" onClick={this.handleDelete}>
          {"Delete Question"}
        </Button>

        <Button variant="contained" onClick={this.handleTrain} disabled={this.state.isTrainButtonDisabled}>
        {this.state.isTrainButtonDisabled && (
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
          {"Train Instead"}
        </Button>
        </Stack>

                
      </CardContent>
    
    </Card>
    );
  }
}

function getQuestions() {

    return fetch(`${CUSTOM_BACKEND_API_STRING}/questions`, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
     
      return data;
    });
    // setQuestions(["1","2","3"]);
}

function Admin(props) {
 
  //todo: make a request to refresh the 
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [isTraining, setIsTraining] = useState(false)

  useEffect(() => {
    getQuestions()
    .then((data) => {
      setQuestions(data)
    })
  }, []);


  return (
    <div>
      <Navbar/>
      <div style={leftBox}>
      {/* <div class="dropdown"> */}
        {/* <button style = {questionDropdown}  class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          New Question
        </button> */}
        {/* <div class="dropdown-menu" style={{ padding:5}} aria-labelledby="dropdownMenuButton"> */}
       
        <List sx={{ width: '100%', maxWidth: 360 }}>
        {questions.map((question) => (
        <ListItem>
        <Question class="dropdown-menu" history = {props.history} questionObject={question} updateFunc={(data)=>{setQuestions(data)}} setSelectedQuestion = {setSelectedQuestion} />
        </ListItem>
        ))}
        
        </List>
        
        {/* </div> */}
      {/* </div> */}
      </div>
      <div id="mainDiv" style={{ width: "80%", height: "80%", float: "right", padding: 40}}>
        {selectedQuestion}
      </div>
      
    </div>
  );

  

}

const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};

const leftBox = {
  width: "20%",
  height: "42em",
  float: "left",
  maxHeight: "42em",
  backgroundColor: "grey",
  overflow: "scroll",
  overflowX: "hidden"
  // opacity: 0.5, 
}

const questionDropdown = {
  width: "11em",
}
export default Admin;
