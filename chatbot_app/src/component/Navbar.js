
import "../App.css";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";

export function Navbar() {
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
            <a class="dropdown-item">
              <Link to="/admin_portal">Admin Login</Link>
            </a>

            <a class="dropdown-item">
              <Link to="/upload_data">Upload Data</Link>
            </a>

            <a class="dropdown-item">
              <Link to="/report_issue">Report Issue</Link>
            </a>

          </div>
        </div>
        <h1 id="homepageTitle">IRPA ChatBot</h1>
      </nav>
    )

}



const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};


