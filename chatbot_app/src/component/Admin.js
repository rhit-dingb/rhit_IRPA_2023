import React, { Component, useEffect, useState } from "react";
import * as ReactDOM from 'react-dom'
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
import {CUSTOM_BACKEND_API_STRING} from "../constants/constants"
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
    const answerPage = (<QuestionAnswer questionObj = {this.props.questionObject}/>);
    ReactDOM.render(answerPage, document.getElementById("mainDiv"));
  }

  render() {
    return <button onClick={this.handleClick}>{this.props.questionObject.content}</button>;
  }
}

class QuestionAnswer extends React.Component {
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleClick() {
    //make api call here
    var inputtedAnswer = document.getElementById("answerInput").value;
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
        getQuestions().then((data) => {this.props.updateFunc(data)});
        // ReactDOM.render(null, document.getElementById("mainDiv"));
        window.location.reload(false);
      });
      // ReactDOM.render(null, document.getElementById("mainDiv"));
    }
  }

  handleDelete() {
    fetch(`${CUSTOM_BACKEND_API_STRING}/question_delete/${this.props.questionObj._id.$oid}`, {
      method: 'DELETE',
    })
    .then(response => response.json)
    .then(data => {
      console.log(data)
      // ReactDOM.render(null, document.getElementById("mainDiv"));
      window.location.reload(false);
    });
  }

  render() {
    return (
      <div>
        <h5>{this.props.questionObj.content}</h5>
        <div id="warningText"></div>
        <input id="answerInput" type="text" placeholder="Enter answer text"></input>
        <button onClick={this.handleClick}>
          {"Submit"}
        </button>
        <button onClick={this.handleDelete}>
          {"Delete Question"}
        </button>
      </div>
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
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand">
          <img
            style={roseIconStyle}
            src={rose_icon}
            alt="Rose-Hulman Institute of Technology"
          />
        </a>

        <div class="dropdown navbar-brand">
          <button
            class="btn"
            type="button"
            id="dropdownMenuLink"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <a class="dropdown-item">
              <Link to="/admin_portal">Admin Login</Link>
            </a>
            <a class="dropdown-item">
              <Link to="/report_issue">Report Issue</Link>
            </a>
          </div>
        </div>
        <h1 id="homepageTitle">IRPA ChatBot</h1>
      </nav>
      <div style={leftBox}>
      <div class="dropdown">
        <button style = {questionDropdown} class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          New Question
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          {questions.map((question) => (<Question class="dropdown-menu" questionObject={question} updateFunc={(data)=>{setQuestions(data)}} />))}
        </div>
      </div>
      </div>
      <div id="mainDiv" style={{ width: "80%", height: "42em", float: "right" }}>
        right content in there
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
