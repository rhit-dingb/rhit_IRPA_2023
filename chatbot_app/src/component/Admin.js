import React, { Component, useEffect, useState } from "react";
import * as ReactDOM from 'react-dom'
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
import {CUSTOM_BACKEND_API_STRING} from "../constants/constants"
import { Navbar } from "./Navbar";


import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';

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
    const answerPage = (<QuestionAnswer questionObj = {this.props.questionObject} updateFunc ={this.props.updateFunc} setSelectedQuestion = {this.props.setSelectedQuestion}/>);
    // ReactDOM.render(answerPage, document.getElementById("mainDiv"));
    this.props.setSelectedQuestion(answerPage)
  }

  render() {
    return <button key ={this.props.questionObject.content} style={{ height:30, maxWidth:250, margin:"auto", borderColor: this.props.questionObject.is_addressed ? 'white' : 'red' }} onClick={this.handleClick}><div style={{textOverflow: "ellipsis", overflow: "hidden", whiteSpace: "nowrap"}}>{this.props.questionObject.content}</div></button>;
  }
}

class QuestionAnswer extends React.Component {
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
   
    this.state = {
      question:props.questionObj.content,
      answer: props.questionObj.answer,
      notificationMessage: "",
      showNotificationMessage: false,
      chatbotAnswers: props.questionObj.chatbotAnswers
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.questionObj !== this.props.questionObj) {
      this.setState({
         question : nextProps.questionObj.content, 
         answer: nextProps.questionObj.answer,
         chatbotAnswers: nextProps.questionObj.chatbotAnswers,
         notificationMessage: "",
         showNotificationMessage: false
        
      });
    }
  }
  
  

  handleClick(e) {
    //make api call here

    e.preventDefault()
    var inputtedAnswer = document.getElementById("answerInput").value;
    console.log("ANSWER")
    // console.log(inputtedAnswer);
    if(inputtedAnswer.trim().length <= 0) {
      document.getElementById("warningText").innerHTML = "Please enter an answer";
    } else {
      // console.log("question 1 submitted");
      console.log(this.props.questionObj._id.$oid);
      fetch(`${CUSTOM_BACKEND_API_STRING}/question_update/${this.props.questionObj._id.$oid}?answer=${document.getElementById("answerInput").value}`, {
        method: 'PUT',
      })
      .then(response => response.json)
      .then(data => {
        console.log(data)
        getQuestions().then((data) => {
          this.props.updateFunc(data)
          this.setState(prevState => ({
            notificationMessage: "Answer updated successfully!",
            showNotificationMessage: true
          }));


        });

        // ReactDOM.render(null, document.getElementById("mainDiv"));
        // window.location.reload(false);
      });
      // ReactDOM.render(null, document.getElementById("mainDiv"));
    }
  }

  handleDelete(e) {
    e.preventDefault()
    fetch(`${CUSTOM_BACKEND_API_STRING}/question_delete/${this.props.questionObj._id.$oid}`, {
      method: 'DELETE',
    })
    .then(response => response.json)
    .then(data => {
      console.log(data)
      getQuestions().then((data) => {
        this.props.updateFunc(data)
        this.props.setSelectedQuestion(null)
          this.setState(prevState => ({
            notificationMessage: "Questions deleted successfully!",
            showNotificationMessage: true
        }))
      })

      // ReactDOM.render(null, document.getElementById("mainDiv"));
      // window.location.reload(false);
    });
  }

  render() {
    return (
      <Card >
      <CardContent sx={{backgroundColor:"#E7EBF0"}}>
      {/* <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
          Question
        </Typography> */}
         {this.state.showNotificationMessage && <Alert severity={"success"} onClose={() => { this.setState(prevState => ({
            showNotificationMessage: false
          })) 
          
          }}>{this.state.notificationMessage}</Alert>}

        <h5>Question</h5>
        <div style={{textOverflow: "ellipsis", overflow: "scroll", marginBottom:50, "overflowX": "hidden"}} >
          <h5 >{this.state.question}</h5>
        </div>
        <div id="warningText"></div>
        <div class="form-floating">
        <h5>Chatbot Answer</h5>
        <div style={{textOverflow: "ellipsis", overflow: "scroll", marginBottom:50, "overflowX": "hidden"}} >
          {this.state.chatbotAnswers? this.state.chatbotAnswers.map((elem)=>{
            console.log(elem)
            return <h5>{elem}</h5>
          })
          : <h5>No answer from chatbot</h5>}
        </div>


        <h5>Answer</h5>
        <textarea id="answerInput" class="form-control" value={this.state.answer || ""} onChange={e => this.setState({ answer : e.target.value })} placeholder="Provide answer here" style={{minHeight:150, maxHeight:300,minWidth: "100%",  maxWidth: "100%", textAlign: "center",  }}    />
        
      </div>
        {/* <input id="answerInput" type="text" placeholder="Enter answer text"></input> */}
        <button onClick={this.handleClick}>
          {"Submit"}
        </button>
        <button onClick={this.handleDelete}>
          {"Delete Question"}
        </button>

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
      console.log("questions" + data);
      return data;
    });
    // setQuestions(["1","2","3"]);
  
}

function Admin() {
  //todo: make a request to refresh the 
  const [questions, setQuestions] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  // const getQuestions = () => {
  //   fetch(`${CUSTOM_BACKEND_API_STRING}/questions`, {
  //     method: 'GET'
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log("questions" + data);
  //     return data;
  //   });
  // }
  // useEffect(() => {
  //   fetch(`${CUSTOM_BACKEND_API_STRING}/questions`, {
  //     method: 'GET'
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     console.log(data);
  //     setQuestions(data);
  //   });
  //   // setQuestions(["1","2","3"]);
  // }, []);
  // console.log("GOT" + getQuestions().then((data) => {setQuestions(data)}));
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
      <div class="dropdown">
        <button style = {questionDropdown}  class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          New Question
        </button>
        <div class="dropdown-menu" style={{ padding:5}} aria-labelledby="dropdownMenuButton">
          {questions.map((question) => (<Question class="dropdown-menu" questionObject={question} updateFunc={(data)=>{setQuestions(data)}} setSelectedQuestion = {setSelectedQuestion} />))}
        </div>
      </div>
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
  backgroundColor: "grey",
  opacity: 0.5, 
}

const questionDropdown = {
  width: "11em",
}
export default Admin;
