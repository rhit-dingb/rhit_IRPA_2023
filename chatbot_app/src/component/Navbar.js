
import "../App.css";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";

import React, { Component, useEffect, useState, useRef} from "react";
import {IS_LOGGED_IN_CONSTANT, TOKEN_KEY} from "../constants/constants"
import { useHistory } from 'react-router-dom';
import { logOut } from "../functions/functions";

export function Navbar() {
    const history = useHistory();

    const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY))

    useEffect(() => {
      // console.log("IS LOGGED IN ")
      // console.log(token)
      if (history.location.pathname == "/admin_login"){
        return 
      }

      if (!token) {
        history.push('/');
      }
    }, [history]);

 
    return (
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

          {!token && 
            <a class="dropdown-item">
              <Link to="/admin_login">Admin Login</Link>
            </a>}

          {token? <div><a class="dropdown-item">
              <Link to="/unanswered_questions">Unanswered Questions</Link>
            </a>

            <a class="dropdown-item">
              <Link to="/frequency">Frequency Data</Link>
            </a>

            <a class="dropdown-item">
              <Link to="/">Chatbot</Link>
            </a>
          
            <a class="dropdown-item">
              <Link to="/upload_data">Upload Data</Link>
            </a>

            <a class="dropdown-item">
              <Link to="/report_issue">Report Issue</Link>
            </a>

            <a class="dropdown-item">
              <Link  to="/admin_list">Admin List</Link>
            </a>

            <a class="dropdown-item">
              <Link onClick={(e)=>{logOut(history)}} to="/admin_login">Logout</Link>
            </a>

           
            </div> : null }

          </div>
        </div>
        <h1 id="homepageTitle">IRPA Chatbot</h1>
      </nav>
    )

}



const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};


