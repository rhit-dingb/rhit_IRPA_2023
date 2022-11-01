import React from "react";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
class NewQuestion extends React.Component {
  render() {
    return <div>{this.props.questionContent}</div>;
  }
}

function Admin() {
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
      <h1>This is the Admin Page</h1>
      <div style={{ width: "20%", height: "42em", float: "left" }}>
        left content in here
      </div>
      <div style={{ width: "80%", height: "42em", float: "right" }}>
        right content in there
      </div>
      <NewQuestion questionContent={"Why Rose-Hulman is good?"} />
    </div>
  );
}

const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};

export default Admin;
