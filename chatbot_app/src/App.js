import "./App.css";
import Basic from "./component/Basic";
import rose_icon from "./rose_icon.png";
// import firebase from "firebase/app";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap/js/dist/dropdown";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";
import { Link } from "react-router-dom";
import Home from "./component/Home";
import Admin from "./component/Admin";
import ReportIssue from "./component/ReportIssue";
import UploadData from "./component/UploadData/UploadData"
import AdminLogin from "./component/AdminLogin"
// firebase.initializeApp({
//   apiKey: "AIzaSyDWEnr4gUrMXGIGuSSUdkAgrO4CvHC-JO0",
//   authDomain: "irpa-chabot.firebaseapp.com",
//   projectId: "irpa-chabot",
//   storageBucket: "irpa-chabot.appspot.com",
//   messagingSenderId: "335746217433",
//   appId: "1:335746217433:web:0ae70749db772e742b15c8",
//   measurementId: "G-707FNN5LZD",
// });

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
       
          <Route exact path="/" component={Home} />

      
          {/* Will probably have to rename the component */}
          <Route path="/unanswered_questions" component={Admin} />

          <Route path="/admin_login" component={AdminLogin} />

        
          <Route path="/report_issue" component={ReportIssue} />


          <Route path="/upload_data" component={UploadData} />

          {/* If any route mismatches the upper 
          route endpoints then, redirect triggers 
          and redirects app to home component with to="/" */}
          <Redirect to="/" />
        </Switch>
      </Router>

      {/* <Basic /> */}
    </div>
  );
}

const roseIconStyle = {
  width: "3.7em",
  height: "2em",
};
export default App;
