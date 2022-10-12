import "./App.css";
import Basic from "./component/Basic";
// import firebase from "firebase/app";

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
      <h1>IRPA ChatBot</h1>
      <Basic />
    </div>
  );
}

export default App;
