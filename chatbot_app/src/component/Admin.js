import React, { Component, useEffect, useState } from "react";
import * as ReactDOM from 'react-dom'
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
class Question extends React.Component {
  //todo: this thing
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    //make api call here
    console.log(this.props.questionContent);
    const answerPage = (<QuestionAnswer text = {this.props.questionContent}/>);
    ReactDOM.render(answerPage, document.getElementById("mainDiv"));
  }

  render() {
    return <button onClick={this.handleClick}>{this.props.questionContent}</button>;
  }
}

class QuestionAnswer extends React.Component {
  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    //make api call here
    var inputtedAnswer = document.getElementById("answerInput").value;
    // console.log(inputtedAnswer);
    if(inputtedAnswer.trim().length <= 0) {
      document.getElementById("warningText").innerHTML = "Please enter an answer";
    } else {
      // console.log("question 1 submitted");
      // fetch(`{base_path}/setanswer`, {
      //   method: 'POST',
      //   body: JSON.stringify({
      //     question: this.props.text,
      //     answer: document.getElementById("answerInput").value
      //   })
      // })
      // .then(response => response.json)
      // .then(data => {
      //   print(data)
      //   ReactDOM.render(null, document.getElementById("mainDiv"));
      // });
      ReactDOM.render(null, document.getElementById("mainDiv"));
    }
  }

  render() {
    return (
      <div>
        <h5>{this.props.text}</h5>
        <div id="warningText"></div>
        <input id="answerInput" type="text" placeholder="Enter answer text"></input>
        <button onClick={this.handleClick}>
          {"Submit"}
        </button>
      </div>
    );
  }
}

function Admin() {
  //todo: make a request to refresh the 
  const [questions, setQuestions] = useState([]);
  useEffect(() => {
    console.log("AAA");
    // fetch(`{base_path}/unanswered`)
    // .then(response => response.json)
    // .then(data => setQuestions(data));
    setQuestions(["1","2","3"]);
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
          {/* <Question class="dropdown-menu" questionContent={"Why Rose-Hulman is good?"} />
          <Question class="dropdown-menu" questionContent={"Dummy question 1"} />
          <Question class="dropdown-menu" questionContent={"Dummy question 2"} /> */}
          {questions.map((question) => (<Question class="dropdown-menu" questionContent={question} />))}
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
