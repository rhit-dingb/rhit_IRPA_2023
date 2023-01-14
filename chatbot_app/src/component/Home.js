import "../App.css";
import Basic from "./Basic";
import rose_icon from "../rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import { Link } from "react-router-dom";
import {Navbar} from "./Navbar"
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
      <Navbar/>
      <Basic />
    </div>
  );
}

const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};
export default Home;
