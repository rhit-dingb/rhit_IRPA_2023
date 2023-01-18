import React from "react";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
import {Navbar} from "./Navbar"

class Question extends React.Component {

  constructor(props) {
    super(props);
    // This binding is necessary to make `this` work in the callback
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick() {
    console.log("question 1 clicked");
  }

  render() {
    return <button onClick={this.handleClick}>{this.props.questionContent}</button>;
  }
}

function Admin() {
  return (
    <div>
      <Navbar/>
      <div style={leftBox}>
      <div class="dropdown">
        <button style = {questionDropdown} class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          New Question
        </button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <Question class="dropdown-menu" questionContent={"Why Rose-Hulman is good?"} />
          <Question class="dropdown-menu" questionContent={"Dummy question 1"} />
          <Question class="dropdown-menu" questionContent={"Dummy question 2"} />
        </div>
      </div>
      </div>
      <div style={{ width: "80%", height: "42em", float: "right" }}>
        right content in there
      </div>
      
    </div>
  );
}



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
