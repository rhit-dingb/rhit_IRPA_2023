import "../App.css";
import Basic from "./Basic";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
// firebase.initializeApp({
//   apiKey: "AIzaSyDWEnr4gUrMXGIGuSSUdkAgrO4CvHC-JO0",
//   authDomain: "irpa-chabot.firebaseapp.com",
//   projectId: "irpa-chabot",
//   storageBucket: "irpa-chabot.appspot.com",
//   messagingSenderId: "335746217433",
//   appId: "1:335746217433:web:0ae70749db772e742b15c8",
//   measurementId: "G-707FNN5LZD",
// });

function Home() {
  return (
    <div className="Home">
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
      <Basic />
    </div>
  );
}

const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};
export default Home;
